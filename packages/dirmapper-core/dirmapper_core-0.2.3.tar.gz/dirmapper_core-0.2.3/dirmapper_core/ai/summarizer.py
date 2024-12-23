# src/dirmapper/ai/summarizer.py
import copy
import os
from typing import List, Optional, Tuple, Dict
from dirmapper_core.formatter.formatter import Formatter
from dirmapper_core.models.directory_item import DirectoryItem
from dirmapper_core.models.directory_structure import DirectoryStructure
from dirmapper_core.styles.tree_style import TreeStyle
from dirmapper_core.utils.logger import logger, log_periodically, stop_logging
from dirmapper_core.writer.template_parser import TemplateParser
from openai import OpenAI, AuthenticationError
from dirmapper_core.utils.paginator import DirectoryPaginator
from dirmapper_core.utils.text_analyzer import TextAnalyzer

import json
import threading
import string
import math

class DirectorySummarizer:
    """
    Class to summarize a directory structure using the OpenAI API or local model.
    """
    def __init__(self, config: dict):
        """
        Initialize the DirectorySummarizer object.

        Args:
            config (dict): Configuration dictionary containing:
                - use_local (bool): Whether to use local summarization.
                - api_token (str): OpenAI API token (required if use_local is False).
                - summarize_file_content (bool): Whether to summarize file contents.
                - max_file_summary_words (int): Maximum words for file content summaries.
                - max_short_summary_characters (int): Maximum characters for short summaries.
                - exclude_files (List[str]): List of files to exclude from summarization.
                - exclude_dirs (List[str]): List of directories to exclude from summarization.
                - exclude_extensions (List[str]): List of file extensions to exclude from summarization.
                - allowed_extensions (List[str]): List of file extensions to allow for summarization.
                - allowed_files (List[str]): List of file names to allow for summarization.
                - pagination_threshold (int): Threshold for pagination (i.e., max items per page allowed).
                - entropy_threshold (float): Threshold for entropy to detect binary content.
                - use_level_pagination (bool): Whether to use level-based pagination.
        """
        self.is_local = config.get('use_local', True)
        self.client = None
        self.summarize_file_content = config.get('summarize_file_content', False)
        self.max_short_summary_characters = config.get('max_short_summary_characters', 75)
        self.max_file_summary_words = config.get('max_file_summary_words', 50)
        self.file_summarizer = FileSummarizer(config)  # Kept this
        self.paginator = DirectoryPaginator(max_items_per_page=config.get('pagination_threshold', 50), max_tokens=4000)
        self.exclude_files = config.get('exclude_files')
        self.exclude_dirs = config.get('exclude_dirs')
        self.exclude_extensions = config.get('exclude_extensions')
        self.allowed_extensions = config.get('allowed_extensions', ['.py', '.md', '.txt', '.json', '.yaml', '.yml', '.toml', '.xml', '.js', '.html', '.css', '.go', '.java'])
        self.allowed_files = config.get('allowed_files', ['README', 'MANIFEST', 'LICENSE', 'CHANGELOG', 'CONTRIBUTING', 'Makefile', 'Dockerfile'])
        self.text_analyzer = TextAnalyzer(
            entropy_threshold=config.get('entropy_threshold', 4.0)
        )
        self.use_level_pagination = config.get('use_level_pagination', False)

        if not self.is_local:
            api_token = config.get("api_token")
            if not api_token:
                raise ValueError("API token is not set. Please set the API token in the preferences.")
            self.client = OpenAI(api_key=api_token)

    def summarize(self, directory_structure: DirectoryStructure) -> str:
        """
        Summarizes the directory structure using the OpenAI API or local model.

        Args:
            directory_structure (DirectoryStructure): The directory structure to summarize.

        Returns:
            str: The directory structure with summaries for each file/folder in the specified format.
        
        Example:
            Parameters:
                directory_structure = DirectoryStructure() # Initialized DirectoryStructure object
            
            Result:
                {
                    "dir1/": {
                        "file1.txt": {
                            "summary": "This file contains the data for the first task.",
                            "short_summary": "This file contains the data for the first task."
                        },
                        "file2.txt": {
                            "summary": "This file contains the data for the second task.",
                            "short_summary": "This file contains the data for the second task."
                        },
                        "subdir1/": {
                            "file3.txt": {
                                "summary": "This file contains the data for the third task.",
                                "short_summary": "This file contains the data for the third task."
                            }
                        }
                    }
        """
        if self.is_local:
            logger.warning('Localized summary functionality under construction. Set preferences to use the api by setting `is_local` to False.')
            return {}

        # Get metadata from first item in directory structure
        meta_data = {
            'root_path': directory_structure.items[0].path if directory_structure.items else ''
        }

        logger.info(f"Summarizing directory structure for {len(directory_structure.items)} items.  {len(directory_structure.get_files())} files, {len(directory_structure.get_directories())} directories.")
        # Summarize the structure
        summarized_structure = self._summarize_api(directory_structure, meta_data)

        # Merge summaries back into the original structure
        if isinstance(summarized_structure, dict):
            directory_structure.merge_nested_dict(summarized_structure)

        return summarized_structure

    def _summarize_api(self, directory_structure: DirectoryStructure, meta_data: dict) -> dict:
        """
        Summarizes the directory structure using the OpenAI API.

        Args:
            directory_structure (DirectoryStructure): The directory structure to summarize.
            meta_data (dict): Metadata about the directory structure.

        Returns:
            dict: The summarized directory structure with summaries in __keys__.content.
        """
        root_path = meta_data.get('root_path', '')
        
        # Preprocess to add content summaries if enabled
        if self.summarize_file_content:
            self._preprocess_structure(directory_structure)
        
        logger.debug("Preprocessed structure:", directory_structure)
        
        # Check if pagination is needed
        should_paginate, estimated_tokens = self.paginator.should_paginate(directory_structure)
        
        if should_paginate:
            logger.info(f"Directory structure requires pagination. Items: {len(directory_structure.items)}, "
                       f"Estimated tokens: {estimated_tokens}")
            paginated_structures = self.paginator.paginate(
                directory_structure, 
                by_level=self.use_level_pagination
            )
            
            if self.use_level_pagination:
                logger.info(f"Using level-based pagination. Processing {len(paginated_structures)} levels")
            else:
                logger.info(f"Using item-based pagination. Processing {len(paginated_structures)} pages")
            
            summarized_structure = {}
            total_pages = len(paginated_structures)
            
            for idx, paginated_structure in enumerate(paginated_structures, 1):
                if self.use_level_pagination:
                    level = len(paginated_structure.items[0].path.split('/')) - 1 if paginated_structure.items else 0
                    logger.info(f"Processing level {level} (page {idx}/{total_pages})")
                    logger.info(f"Current level contains {len(paginated_structure.items)} items")
                else:
                    logger.info(f"Processing page {idx}/{total_pages}")
                    logger.info(f"Current page contains {len(paginated_structure.items)} items")
                
                # Log the first few items in this batch for context
                sample_items = [item.path for item in paginated_structure.items[:3]]
                logger.debug(f"Sample items in current batch: {', '.join(sample_items)}")
                
                partial_summary = self._summarize_directory_structure_api(
                    paginated_structure,
                    self.max_short_summary_characters     
                )
                summarized_structure = self._merge_summaries(summarized_structure, partial_summary)
                logger.info(f"Completed processing batch {idx}/{total_pages}")
            
            return summarized_structure
        else:
            logger.info(f"Processing directory structure without pagination. Items: {len(directory_structure.items)}, "
                       f"Estimated tokens: {estimated_tokens}")
            return self._summarize_directory_structure_api(
                directory_structure, 
                self.max_short_summary_characters
            )

    def _preprocess_structure(self, structure: DirectoryStructure) -> None:
        """
        Preprocesses the directory structure to add content summaries in __keys__.content.
        Modifies the structure in place.

        Args:
            structure (DirectoryStructure): The directory structure to preprocess
        """
        for item in structure.items:
            # Compute content hash for all files
            content_hash = item.content_hash

            # Summarize content if it's a file
            if item.metadata.get('type') == 'file':
                if self._is_empty_or_near_empty(item.content):
                    item.summary = "Empty File"
                    item.short_summary = "Empty File"
                elif self._should_summarize_file(item.path, item.content):
                    summary_dict = self.file_summarizer.summarize_content(item, self.max_file_summary_words)
                    item.summary = summary_dict.get('summary', '')
                    item.short_summary = summary_dict.get('short_summary', '')
    
    def _is_empty_or_near_empty(self, content: Optional[str]) -> bool:
        """
        Check if the content is empty or near-empty.

        Args:
            content (Optional[str]): The content to check.

        Returns:
            bool: True if the content is empty or near-empty, False otherwise.
        """
        return content is None or len(content.strip()) == 0

    def _should_summarize_file(self, file_path: str, content: Optional[str] = None) -> bool:
        """
        Determines if a file should be summarized based on its extension and content characteristics.

        Args:
            file_path (str): The path to the file.
            content (Optional[str]): The content of the file.

        Returns:
            bool: True if the file should be summarized, False otherwise.
        """
        if self.exclude_files and os.path.basename(file_path) in self.exclude_files:
            return False
        if self.exclude_dirs and os.path.dirname(file_path) in self.exclude_dirs:
            return False
        if self.exclude_extensions and os.path.splitext(file_path)[1] in self.exclude_extensions:
            return False
        
        # Check file extension and name
        _, ext = os.path.splitext(file_path)
        file_name = os.path.basename(file_path)
        if ext.lower() in self.allowed_extensions or file_name in self.allowed_files:
            # Even if extension is allowed, check if content is binary
            print("checking:", file_name)
            return not (content and self.text_analyzer.is_binary_content(content))
        
        return False

    def summarize_directory_structure_local(self, directory_structure: str, short_summary_length: int) -> dict:
        """
        Summarizes the directory structure using a local model.

        Args:
            directory_structure (str): The directory structure to summarize.
            short_summary_length (int): The maximum word length for each summary.

        Returns:
            dict: The summarized directory structure in JSON format with summaries for each file/folder.
        """
        # Summarize the directory structure using a local model
        try:
            import transformers
            # Load and run the local model for summarization
            # Your summarization code here
        except ImportError:
            # logger.error("Summarization feature requires additional dependencies. Please run `dirmap install-ai` to set it up.")
            return "Error: Summarization feature requires additional dependencies.  Please run `dirmap install-ai` to set it up."

    def _summarize_directory_structure_api(self, directory_structure: DirectoryStructure, short_summary_length: int) -> dict:
        """
        Summarizes the directory structure using the OpenAI API.

        Args:
            directory_structure (DirectoryStructure): The directory structure to summarize with __keys__.
            short_summary_length (int): The maximum character length for each summary.

        Returns:
            dict: The summarized directory structure in JSON format with summaries in __keys__.content.
        """
        simple_json_structure = directory_structure.to_nested_dict(['type', 'short_summary'])
        tree_structure = TreeStyle.write_structure(directory_structure)
        logger.info("Simple JSON Structure: " + json.dumps(simple_json_structure, indent=2))

        messages = [
            {
                "role": "system",
                "content": "You are a directory structure analyzer. Respond only with valid JSON."
            },
            {
                "role": "user", 
                "content": (
                    "Analyze the following directory structure:\n\n"
                    f"{tree_structure}\n\n"
                    "Use the following JSON object that matches the input structure to generate "
                    "`short_summary` fields overwriting the existing `short_summary` field. Use the existing `short_summary` value "
                    "for additional context about the existing file if it is not labled 'Empty File'. Generate a short summary for "
                    "each folder based on the files it contains and also store this in the field `short_summary`. "
                    f"Do not modify the structure in any other way. Write each short summary in {short_summary_length} characters "
                    f"or less. Here is the formatted JSON:\n\n{json.dumps(simple_json_structure, indent=2)}"
                )
            }
        ]
        logger.info("Sending request to API for summarization...")
        logger.info(f"Structure contains {len(directory_structure.items)} items "
                   f"({len(directory_structure.get_files())} files, "
                   f"{len(directory_structure.get_directories())} directories)")

        stop_logging.clear()
        logging_thread = threading.Thread(
            target=log_periodically, 
            args=("Waiting for response from OpenAI API...", 5)
        )
        logging_thread.start()

        try:
            response = self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=messages,
                temperature=0.3,  # Lower temperature for more consistent output
                max_tokens=4096,
                response_format={"type": "json_object"}
            )
            
            if not response.choices:
                logger.error("No response from API")
                return directory_structure
                
            # Log the raw response for debugging
            raw_response = response.choices[0].message.content
            logger.debug(f"Raw API Response:\n{raw_response[:500]}...")  # First 500 chars
            
            try:
                summaries = json.loads(raw_response)
                logger.debug("Summaries in _summarize_dir_struct_api:", json.dumps(summaries, indent=2))
                logger.info("Successfully parsed API response")
                return summaries
            except json.JSONDecodeError as e:
                logger.error(f"JSON Parse Error at position {e.pos}: {raw_response[max(0, e.pos-200):e.pos+200]}")
                return directory_structure
                
        except Exception as e:
            logger.error(f"API Error: {str(e)}")
            return directory_structure
            
        finally:
            stop_logging.set()
            logging_thread.join()
    
    def _merge_summaries(self, original: dict, new: dict) -> dict:
        """
        Merges two dictionaries of summaries as a deep merge.

        Args:
            original (dict): The original dictionary of summaries.
            new (dict): The new dictionary of summaries to merge.

        Returns:
            dict: Returns the merged dictionary of summaries (which is also mutated in place).
        """
        for key, value in new.items():
            if key in original and isinstance(original[key], dict) and isinstance(value, dict):
                original[key] = self._merge_summaries(original[key], value)
            else:
                original[key] = value
        return original

class FileSummarizer:
    """
    Class to summarize a file's content using the OpenAI API or a local model.
    """
    def __init__(self, config: dict):
        """
        Initialize the FileSummarizer object.

        Args:
            config (dict): The config for the summarizer.
        """
        self.is_local = config.get("use_local", False)
        self.max_file_summary_words = config.get("max_file_summary_words", 50)
        self.max_short_summary_characters = config.get("max_short_summary_characters", 75)
        self.client = None
        if not self.is_local:
            api_token = config.get("api_token")
            if not api_token:
                raise ValueError("API token is not set. Please set the API token in the preferences.")
            self.client = OpenAI(api_key=api_token)

    def summarize_content(self, item: DirectoryItem, max_words: int = 100, force_refresh: bool = False) -> dict:
        """
        Summarizes the content using the OpenAI API or local model.

        Args:
            item (DirectoryItem): The content to summarize.
            max_words (int): The maximum number of words for the summary.
            force_refresh (bool): Whether to force refresh the cache.

        Returns:
            dict: The summarized content with the summary and short summary.
        """
        # Compute content hash
        content_hash = item.content_hash

        # Get content
        content = item.content
        if content is None:
            return {}

        # Check if the file should be summarized
        if not force_refresh and item.summary and item.content_hash == content_hash:
            logger.info(f"Using cached summary for {item.name}")
            return {'summary': item.summary, 'short_summary': item.short_summary}

        if self.is_local:
            logger.warning('Local summarization is not implemented yet.')
            return {"summary": "Local summarization is not implemented yet.", "short_summary": ""}
        else:
            # Check content size
            max_content_length = 5000  # Adjust based on API limits
            if len(content) > max_content_length:
                logger.info(f"File is large; summarizing in chunks. Summarizing {item.name or 'content'}...")
                summary_dict = self._summarize_large_content(item.name, content, max_words)
                summary = summary_dict.get('summary', '')
                short_summary = summary_dict.get('short_summary', '')
            else:
                summary_dict = self._summarize_purpose_api(item.name, content, max_words)
                summary = summary_dict.get('summary', '')
                short_summary = summary_dict.get('short_summary', '')
            
            item.summary = summary
            item.short_summary = short_summary  # Add short summary
            item.content_hash = content_hash  # Update the hash in the item
            return {'summary': summary, 'short_summary': short_summary}

    def summarize_file(self, file_path: str, max_words: int = 100) -> dict:
        """
        Summarizes the content of a file.

        Args:
            file_path (str): The path to the file to summarize.
            max_words (int): The maximum number of words for the summary.

        Returns:
            dict: The summarized content with the summary and short summary.
        """
        if not os.path.isfile(file_path):
            logger.error(f"File not found: {file_path}")
            return {"summary": "", "short_summary": ""}

        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read()
        except Exception as e:
            logger.error(f"Error reading file {file_path}: {e}")
            return {"summary": "", "short_summary": ""}

        if self.is_local:
            logger.warning('Local summarization is not implemented yet.')
            return {"summary": "Local summarization is not implemented yet.", "short_summary": ""}
        else:
            file_name = os.path.basename(file_path)
            # Check content size
            max_content_length = 5000  # Adjust based on API limits
            if len(content) > max_content_length:
                logger.info(f"File is large; summarizing in chunks. Summarizing {file_name}...")
                return self._summarize_large_content(content, max_words)
            else:
                return self._summarize_purpose_api(file_name, content, max_words)

    def _summarize_large_content(self, file_name: str, content: str, max_words: int) -> dict:
        """
        Summarizes large content by splitting it into chunks.

        Args:
            file_name (str): The name of the file.
            content (str): The content to summarize.
            max_words (int): The maximum number of words for the summary.

        Returns:
            dict: The combined summary of all chunks and a short summary.
        """
        chunk_size = 4000  # Adjust based on API limits
        chunks = [content[i:i + chunk_size] for i in range(0, len(content), chunk_size)]
        summaries = []

        for idx, chunk in enumerate(chunks):
            logger.info(f"Summarizing chunk {idx + 1}/{len(chunks)}")
            summary_dict = self._summarize_purpose_api(file_name, chunk, max_words)
            summaries.append(summary_dict.get('summary', ''))

        # Combine summaries
        combined_summary = "\n".join(summaries)
        
        # Summarize the combined summary based on max_words guidelines
        combined_summary = self._summarize_purpose_api(file_name, combined_summary, max_words).get('summary', '')

        print("Combined Summary: ", combined_summary)
        logger.info(f"Final Combined Summary Length: {len(combined_summary)}")
        # Generate a short summary
        short_summary = self._summarize_purpose_api(file_name, combined_summary, self.max_short_summary_characters, is_short=True).get('short_summary', '')
        print("Short Summary: ", short_summary)

        return {'summary': combined_summary, 'short_summary': short_summary}
    
    def _summarize_purpose_api(self, file_name: str, content: str, max_length: int, is_short: bool=False) -> dict:
        """
        Summarizes the content using the OpenAI API.

        Args:
            file_name (str): The name of the file.
            content (str): The content to summarize.
            max_length (int): The maximum length for the summary (words or characters).
            is_short (bool): Whether the summary is a short summary.

        Returns:
            dict: The summarized content with the summary and short summary.
        """
        max_tokens = 2048
        temperature = 0.5
        model = "gpt-4o-mini"

        # Prepare the prompt
        messages = [
            {"role": "system", "content": "You are a helpful assistant that summarizes file content into markdown format."},
            {"role": "user", "content": (
                f"Please provide a JSON response with both a long summary and a short summary of the following file content. "
                "The long summary should be a brief description of the content, and the short summary should be a concise version of the long summary. "
                "Explain the purpose of the content and any key points. "
                f"The long summary should be limited to {self.max_file_summary_words} words and the short summary should be limited to {self.max_short_summary_characters} characters. "
                "Short summaries should not have any new lines. Return the summaries in the following format:\n\n"
                f"{{\n  \"summary\": \"This is the long summary.\",\n  \"short_summary\": \"This is the short summary.\"\n}}"
                f"Do not include any additional information in the response. Here is the content for the file {file_name}:\n\n"
                f"{content}"
            )}
        ]

        logger.info(f"Sending request to OpenAI API for summarization. Summarizing {file_name}...")

        stop_logging.clear()
        logging_thread = threading.Thread(target=log_periodically, args=("Waiting for response from OpenAI API...", 5))
        logging_thread.start()

        try:
            response = self.client.chat.completions.create(
                model=model,
                messages=messages,
                max_tokens=max_tokens,
                temperature=temperature,
                response_format={"type": "json_object"}
            )
            if not response or not response.choices:
                logger.error("Empty or invalid response from API")
                return {"summary": "", "short_summary": ""}

            summary_response = response.choices[0].message.content.strip()
            try:
                summary_dict = json.loads(summary_response)
                return {
                    "summary": summary_dict.get("summary", ""),
                    "short_summary": summary_dict.get("short_summary", "")
                }
            except json.JSONDecodeError:
                logger.error("Failed to parse JSON response from API")
                return {"summary": "", "short_summary": ""}
        except AuthenticationError as e:
            logger.error(f"Authentication error: {e}")
            return {"summary": "", "short_summary": ""}
        except Exception as e:
            logger.error(f"Error during API call: {e}")
            return {"summary": "", "short_summary": ""}
        finally:
            stop_logging.set()
            logging_thread.join()