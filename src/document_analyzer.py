"""
Document Analysis Module
Handles document text extraction and AI-powered legal analysis
"""

import os
import logging
from typing import Dict, Any
import PyPDF2
import docx
from openai import OpenAI

logger = logging.getLogger(__name__)


class DocumentAnalyzer:
    """Main class for document analysis operations"""
    
    def __init__(self):
        """Initialize the document analyzer with OpenAI client"""
        api_key = os.getenv('OPENAI_API_KEY')
        if not api_key:
            logger.warning("OpenAI API key not found. Analysis will use mock responses.")
            self.client = None
        else:
            self.client = OpenAI(api_key=api_key)
    
    def extract_text(self, filepath: str) -> str:
        """Extract text from document based on file type"""
        try:
            file_extension = filepath.lower().split('.')[-1]
            
            if file_extension == 'pdf':
                return self._extract_pdf_text(filepath)
            elif file_extension == 'docx':
                return self._extract_docx_text(filepath)
            elif file_extension == 'txt':
                return self._extract_txt_text(filepath)
            else:
                raise ValueError(f"Unsupported file type: {file_extension}")
                
        except Exception as e:
            logger.error(f"Text extraction failed: {str(e)}")
            raise
    
    def _extract_pdf_text(self, filepath: str) -> str:
        """Extract text from PDF file"""
        text = ""
        with open(filepath, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            for page in pdf_reader.pages:
                text += page.extract_text() + "\n"
        return text.strip()
    
    def _extract_docx_text(self, filepath: str) -> str:
        """Extract text from DOCX file"""
        doc = docx.Document(filepath)
        text = ""
        for paragraph in doc.paragraphs:
            text += paragraph.text + "\n"
        return text.strip()
    
    def _extract_txt_text(self, filepath: str) -> str:
        """Extract text from TXT file"""
        with open(filepath, 'r', encoding='utf-8') as file:
            return file.read().strip()
    
    def analyze_document(self, filepath: str) -> Dict[str, Any]:
        """Analyze document and return legal insights"""
        try:
            # Extract text from document
            text_content = self.extract_text(filepath)
            
            if not text_content.strip():
                return {
                    'error': 'Document appears to be empty or text could not be extracted'
                }
            
            # Perform AI analysis
            analysis = self._perform_legal_analysis(text_content)
            
            return {
                'text_length': len(text_content),
                'word_count': len(text_content.split()),
                'analysis': analysis,
                'success': True
            }
            
        except Exception as e:
            logger.error(f"Document analysis failed: {str(e)}")
            return {
                'error': f'Analysis failed: {str(e)}',
                'success': False
            }
    
    def _perform_legal_analysis(self, text: str) -> Dict[str, Any]:
        """Perform AI-powered legal analysis of the text"""
        if not self.client:
            # Return mock analysis if no OpenAI client
            return self._get_mock_analysis(text)
        
        try:
            # Prepare the prompt for legal analysis
            prompt = self._create_legal_analysis_prompt(text)
            
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a legal document analysis assistant. Provide clear, structured analysis of legal documents."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=1000,
                temperature=0.3
            )
            
            analysis_text = response.choices[0].message.content
            
            return {
                'summary': self._extract_summary(analysis_text),
                'key_points': self._extract_key_points(analysis_text),
                'document_type': self._identify_document_type(text),
                'risks_concerns': self._extract_risks(analysis_text),
                'recommendations': self._extract_recommendations(analysis_text),
                'full_analysis': analysis_text
            }
            
        except Exception as e:
            logger.error(f"AI analysis failed: {str(e)}")
            return self._get_mock_analysis(text)
    
    def _create_legal_analysis_prompt(self, text: str) -> str:
        """Create a structured prompt for legal document analysis"""
        return f"""
        Please analyze the following legal document and provide:
        
        1. SUMMARY: A brief overview of the document's purpose and main content
        2. DOCUMENT TYPE: What type of legal document this appears to be
        3. KEY POINTS: The most important terms, clauses, or provisions
        4. RISKS & CONCERNS: Any potential legal risks or concerning clauses
        5. RECOMMENDATIONS: Suggestions for review or action
        
        Document text:
        {text[:4000]}  # Limit text to avoid token limits
        
        Please structure your response clearly with these sections.
        """
    
    def _extract_summary(self, analysis: str) -> str:
        """Extract summary from analysis text"""
        lines = analysis.split('\n')
        for i, line in enumerate(lines):
            if 'SUMMARY' in line.upper():
                return lines[i+1] if i+1 < len(lines) else "Summary not available"
        return "Summary not available"
    
    def _extract_key_points(self, analysis: str) -> list:
        """Extract key points from analysis text"""
        points = []
        lines = analysis.split('\n')
        in_key_points = False
        
        for line in lines:
            if 'KEY POINTS' in line.upper():
                in_key_points = True
                continue
            elif in_key_points and line.startswith(('RISKS', 'RECOMMENDATIONS', 'DOCUMENT TYPE')):
                break
            elif in_key_points and line.strip():
                points.append(line.strip())
        
        return points[:5]  # Limit to 5 key points
    
    def _identify_document_type(self, text: str) -> str:
        """Identify the type of legal document"""
        text_lower = text.lower()
        
        if 'contract' in text_lower or 'agreement' in text_lower:
            return 'Contract/Agreement'
        elif 'will' in text_lower and 'testament' in text_lower:
            return 'Will/Testament'
        elif 'lease' in text_lower:
            return 'Lease Agreement'
        elif 'nda' in text_lower or 'non-disclosure' in text_lower:
            return 'Non-Disclosure Agreement'
        elif 'employment' in text_lower:
            return 'Employment Document'
        else:
            return 'Legal Document'
    
    def _extract_risks(self, analysis: str) -> list:
        """Extract risks and concerns from analysis text"""
        risks = []
        lines = analysis.split('\n')
        in_risks = False
        
        for line in lines:
            if 'RISKS' in line.upper() or 'CONCERNS' in line.upper():
                in_risks = True
                continue
            elif in_risks and line.startswith(('RECOMMENDATIONS', 'SUMMARY')):
                break
            elif in_risks and line.strip():
                risks.append(line.strip())
        
        return risks[:3]  # Limit to 3 main risks
    
    def _extract_recommendations(self, analysis: str) -> list:
        """Extract recommendations from analysis text"""
        recommendations = []
        lines = analysis.split('\n')
        in_recommendations = False
        
        for line in lines:
            if 'RECOMMENDATIONS' in line.upper():
                in_recommendations = True
                continue
            elif in_recommendations and line.strip():
                recommendations.append(line.strip())
        
        return recommendations[:3]  # Limit to 3 recommendations
    
    def _get_mock_analysis(self, text: str) -> Dict[str, Any]:
        """Provide mock analysis when OpenAI is not available"""
        return {
            'summary': 'Legal document analysis - OpenAI API not configured. This is a sample analysis.',
            'key_points': [
                'Document contains legal terminology',
                'Multiple clauses and provisions identified',
                'Requires professional legal review'
            ],
            'document_type': self._identify_document_type(text),
            'risks_concerns': [
                'Unable to perform detailed risk analysis without AI',
                'Professional legal review recommended'
            ],
            'recommendations': [
                'Configure OpenAI API for detailed analysis',
                'Consult with a qualified attorney',
                'Review all terms carefully'
            ],
            'full_analysis': 'Mock analysis - Please configure OpenAI API key for detailed legal document analysis.'
        }