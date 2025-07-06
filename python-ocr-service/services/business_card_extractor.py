import re
from typing import Dict, List, Optional

class BusinessCardExtractor:
    def __init__(self):
        self.email_pattern = re.compile(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b')
        self.phone_pattern = re.compile(r'(?:\+?\d{1,3}[-.\s]?)?\(?\d{1,4}\)?[-.\s]?\d{1,4}[-.\s]?\d{1,4}[-.\s]?\d{1,9}')
        self.website_pattern = re.compile(r'(?:www\.)?[a-zA-Z0-9][a-zA-Z0-9-]+[a-zA-Z0-9]\.[a-zA-Z]{2,}(?:/[^\s]*)?')
        self.title_keywords = ['CEO', 'CTO', 'CFO', 'COO', 'Director', 'Manager', 'Engineer', 
                              'Developer', 'Designer', 'Analyst', 'Consultant', 'President', 
                              'Vice President', 'VP', 'Executive', 'Senior', 'Lead', 'Head']
    
    def extract_info(self, text_blocks: List[Dict]) -> Dict:
        all_text = ' '.join([block['text'] for block in text_blocks])
        lines = [block['text'] for block in text_blocks]
        
        extracted = {
            'name': self._extract_name(lines),
            'title': self._extract_title(lines),
            'company': self._extract_company(lines),
            'email': self._extract_email(all_text),
            'phone': self._extract_phone(all_text),
            'website': self._extract_website(all_text),
            'address': self._extract_address(lines),
            'raw_text': '\n'.join(lines),
            'confidence': self._calculate_extraction_confidence(text_blocks)
        }
        
        return extracted
    
    def _extract_name(self, lines: List[str]) -> Optional[str]:
        for i, line in enumerate(lines[:5]):
            words = line.split()
            if len(words) >= 2 and len(words) <= 4:
                if all(word[0].isupper() for word in words if len(word) > 1):
                    if not any(keyword in line for keyword in ['Inc', 'LLC', 'Ltd', 'Corp']):
                        return line.strip()
        return None
    
    def _extract_title(self, lines: List[str]) -> Optional[str]:
        for line in lines:
            for keyword in self.title_keywords:
                if keyword.lower() in line.lower():
                    return line.strip()
        return None
    
    def _extract_company(self, lines: List[str]) -> Optional[str]:
        company_keywords = ['Inc', 'LLC', 'Ltd', 'Corporation', 'Corp', 'Company', 'Co.']
        for line in lines:
            for keyword in company_keywords:
                if keyword in line:
                    return line.strip()
        
        for i, line in enumerate(lines[1:6]):
            if len(line) > 3 and line[0].isupper():
                if not self.email_pattern.search(line) and not self.phone_pattern.search(line):
                    if not any(kw in line for kw in self.title_keywords):
                        return line.strip()
        return None
    
    def _extract_email(self, text: str) -> Optional[str]:
        match = self.email_pattern.search(text)
        return match.group(0) if match else None
    
    def _extract_phone(self, text: str) -> Optional[str]:
        matches = self.phone_pattern.findall(text)
        if matches:
            phone = max(matches, key=len)
            phone = re.sub(r'[^\d+\s()-]', '', phone)
            return phone.strip()
        return None
    
    def _extract_website(self, text: str) -> Optional[str]:
        match = self.website_pattern.search(text)
        if match:
            website = match.group(0)
            if not website.startswith('http'):
                website = 'http://' + website
            return website
        return None
    
    def _extract_address(self, lines: List[str]) -> Optional[str]:
        address_keywords = ['Street', 'St', 'Avenue', 'Ave', 'Road', 'Rd', 'Boulevard', 
                           'Blvd', 'Drive', 'Dr', 'Suite', 'Ste', 'Floor']
        address_lines = []
        
        for i, line in enumerate(lines):
            if any(keyword in line for keyword in address_keywords):
                address_lines.append(line)
                if i + 1 < len(lines):
                    next_line = lines[i + 1]
                    if re.search(r'\d{5}', next_line) or any(state in next_line.upper() 
                                                             for state in ['CA', 'NY', 'TX', 'FL']):
                        address_lines.append(next_line)
        
        return ' '.join(address_lines).strip() if address_lines else None
    
    def _calculate_extraction_confidence(self, text_blocks: List[Dict]) -> float:
        if not text_blocks:
            return 0.0
        
        total_confidence = sum(block['confidence'] for block in text_blocks)
        return round(total_confidence / len(text_blocks), 4)