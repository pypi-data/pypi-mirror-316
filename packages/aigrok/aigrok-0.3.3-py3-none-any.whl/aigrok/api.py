"""
API module for PDF processing functionality.
"""
from pathlib import Path
from typing import Optional, Dict, Any, Union, List, Literal
from pydantic import BaseModel, Field, ConfigDict
from loguru import logger
import json
import csv
from io import StringIO
import requests
from pprint import pformat

from .pdf_processor import PDFProcessor, ProcessingResult

class OutputSchema(BaseModel):
    """Schema for structured output."""
    model_config = ConfigDict(strict=True)
    format: Literal["json", "csv", "markdown"] = Field(..., description="Output format (json, csv, or markdown)")
    schema_def: Union[str, List[str]] = Field(..., description="JSON schema example, CSV column names, or markdown template")

class ProcessRequest(BaseModel):
    """Request model for PDF processing."""
    model_config = ConfigDict(
        extra='forbid',
        validate_default=True
    )
    
    file_path: str
    prompt: Optional[str] = None
    output_schema: Optional[OutputSchema] = None

class ProcessResponse(BaseModel):
    """Response model for PDF processing."""
    model_config = ConfigDict(
        extra='forbid',
        validate_default=True
    )
    
    success: bool
    text: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None
    page_count: int = 0
    error: Optional[str] = None
    llm_response: Optional[Any] = None
    structured_output: Optional[str] = None

class APIProcessor:
    """Server-side API processor."""
    
    def __init__(self):
        """Initialize the API processor."""
        self.pdf_processor = PDFProcessor()
    
    def _generate_format_prompt(self, format_type: str, schema: Union[str, List[str]]) -> str:
        """Generate a prompt for formatted output."""
        if format_type == "json":
            return f"""Analyze the document and extract information in the following JSON format.
            Use this example as a template for the structure (field names must match exactly):
            {schema}
            
            Respond ONLY with the JSON data, no other text."""
        elif format_type == "csv":
            columns = ", ".join(schema if isinstance(schema, list) else schema.split(","))
            return f"""Analyze the document and extract information in CSV format with these columns:
            {columns}
            
            Respond ONLY with the CSV data (no headers), with values separated by commas."""
        else:  # markdown
            return f"""Analyze the document and extract information in markdown format using the following template:
            {schema}
            
            Respond ONLY with the markdown text."""
    
    def _validate_structured_output(self, output: str, schema: OutputSchema) -> bool:
        """Validate the structured output against the schema."""
        try:
            if schema.format == "json":
                # Validate JSON structure
                example = json.loads(schema.schema_def if isinstance(schema.schema_def, str) else json.dumps(schema.schema_def))
                result = json.loads(output)
                # Check if all keys in example exist in result
                return all(key in result for key in example.keys())
            elif schema.format == "csv":
                # Validate CSV structure
                expected_columns = len(schema.schema_def if isinstance(schema.schema_def, list) else schema.schema_def.split(","))
                reader = csv.reader(StringIO(output))
                row = next(reader)
                return len(row) == expected_columns
            else:  # markdown
                # No validation for markdown format
                return True
        except Exception:
            return False
    
    def process_pdf(self, request: ProcessRequest) -> ProcessResponse:
        """
        Process a PDF file based on the API request.
        
        Args:
            request: ProcessRequest containing file path and optional prompt
            
        Returns:
            ProcessResponse containing the processing results
        """
        try:
            # Log model information in verbose mode
            logger.debug("Using model configuration:\n%s", pformat({
                "provider": "PDFProcessor",
                "model": self.pdf_processor,
                "capabilities": "PDF processing"
            }))

            # First, extract text from PDF
            result = self.pdf_processor.process_file(
                file_path=request.file_path,
                prompt=request.prompt
            )
            
            # Log response in verbose mode
            logger.debug("PDF Processing Response:\n%s", pformat({
                "success": result.success,
                "text": result.text,
                "metadata": result.metadata,
                "page_count": result.page_count,
                "error": result.error,
                "llm_response": result.llm_response
            }))

            response = ProcessResponse(
                success=result.success,
                text=result.text,
                metadata=result.metadata,
                page_count=result.page_count,
                error=result.error,
                llm_response=result.llm_response
            )
            
            # Handle structured output if schema provided
            if request.output_schema:
                format_prompt = self._generate_format_prompt(
                    request.output_schema.format,
                    request.output_schema.schema_def
                )
                
                # Log request data in verbose mode
                logger.debug("API Request:\n%s", pformat({
                    "prompt": format_prompt,
                    "file_path": request.file_path
                }))

                # Get structured output from LLM
                format_result = self.pdf_processor.process_file(
                    request.file_path,
                    prompt=format_prompt,
                    enforce_pdf=True
                )
                
                # Log response in verbose mode
                logger.debug("API Response:\n%s", pformat({
                    "success": format_result.success,
                    "text": format_result.text,
                    "metadata": format_result.metadata,
                    "page_count": format_result.page_count,
                    "error": format_result.error,
                    "llm_response": format_result.llm_response
                }))

                if format_result.success and format_result.llm_response:
                    structured_output = format_result.llm_response.strip()
                    # Validate the output
                    if self._validate_structured_output(structured_output, request.output_schema):
                        response.structured_output = structured_output
                    else:
                        response.error = "Failed to generate valid structured output"
            
            return response
            
        except Exception as e:
            logger.error(f"Error processing PDF through API: {str(e)}")
            return ProcessResponse(
                success=False,
                error=str(e)
            )

class APIClient:
    """Client for interacting with the PDF processing API."""
    
    def __init__(self, base_url: str = "http://localhost:8000"):
        """Initialize the API client."""
        self.base_url = base_url.rstrip('/')
        
    def process(self, request: ProcessRequest) -> ProcessResponse:
        """Process a PDF file.
        
        Args:
            request: The processing request
            
        Returns:
            The processing response
        """
        try:
            # Log request data in verbose mode
            logger.debug("API Request:\n%s", pformat({
                "file_path": request.file_path,
                "prompt": request.prompt,
                "output_schema": request.output_schema
            }))

            request_data = {"file_path": str(request.file_path), "prompt": request.prompt}
            
            if request.output_schema:
                request_data["output_schema"] = {
                    "format": request.output_schema.format,
                    "schema_def": request.output_schema.schema_def
                }
            
            request = ProcessRequest(**request_data)
            response = requests.post(
                f"{self.base_url}/process",
                json=request.model_dump()
            )
            response.raise_for_status()
            
            # Log response in verbose mode
            logger.debug("API Response:\n%s", pformat(response.json()))

            return ProcessResponse(**response.json())
        except Exception as e:
            logger.error(f"Error processing PDF through API: {str(e)}")
            return ProcessResponse(
                success=False,
                error=str(e)
            ) 