import requests
import json
import os
import re
import time
import uuid
from typing import Optional, Dict, List, Union
from colorama import init, Fore, Style

init()  # Initialize colorama

class MacroImageGenerator:
    def __init__(self, output_dir: str = "generated_images", chat_id: Optional[str] = None):
        """
        Initialize the MacroImageGenerator.
        
        Args:
            output_dir (str): Directory to save generated images
            chat_id (str, optional): Custom chat ID for the conversation. If None, a new one will be created.
        """
        self.output_dir = output_dir
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
            
        self.base_url = "https://chat.mistral.ai/api/chat"
        self.chat_id = chat_id or str(uuid.uuid4())
        self._init_headers()
        
        print(f"{Fore.CYAN}[INFO] Chat URL: https://chat.mistral.ai/chat/{self.chat_id}{Style.RESET_ALL}")
    
    def _init_headers(self):
        """Initialize headers for API requests."""
        self.headers = {
            'accept': '*/*',
            'accept-language': 'ar-AE,ar;q=0.9,en-US;q=0.8,en;q=0.7',
            'content-type': 'application/json',
            'origin': 'https://chat.mistral.ai',
            'referer': f'https://chat.mistral.ai/chat/{self.chat_id}',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        
        self.cookies = {
            'NEXT_LOCALE': 'en',
            'intercom-device-id-xel0jpx9': '79d25b06-b079-49ea-bc4f-9dab1f1700cb',
            'ory_kratos_continuity': 'MTczNDY2NzQ4MXxEWDhFQVFMX2dBQUJFQUVRQUFCZl80QUFBUVp6ZEhKcGJtY01Jd0FoYjNKNVgydHlZWFJ2YzE5dmFXUmpYMkYxZEdoZlkyOWtaVjl6WlhOemFXOXVCbk4wY21sdVp3d21BQ1EzT1RBMllUQmhNeTAyTVdFd0xUUTJaakF0T0dNd05TMDBPR1l5TkdabE1UazNZems9fCsw0VcMzHLBm_3zhYYmYuMeqDYFnQp7TLV0NdmaTl9v',
            'csrf_token_1d61ec8f0158ec4868343239ec73dbe1bfebad9908ad860e62f470c767573d0d': 'jx7PaXVa4eHFLefiu84VoH/M87C8x8913pVkVNuIe2E=',
            'ory_session_coolcurranf83m3srkfl': 'MTczNDY2NzQ4Nnw0aEJaZXprVWJZZEh2NVpfdEU4WklXTHU1dnczRUxTeEdtNEtUOWNmbTdSNmk4aEFvWVVvb2E1N1dWWDU3dmJkNGJtem0xal9keTVCdUZ2MDZwNFFKY2JzQzRtdFBCRTJWQVBEM0dyYmFMaU5sYkRkQ2tjSGJFX25JM2lEZ3BnUGF6NnRBT2N0ajZadGdoWk0tZnJiWWdZN2xKaHZ5czh3LWxtYmZSeTh2WUVXZWtvRlF2QUYtdllqN0ZZQmtFM3V5QlJjVENNZzJoNFdnUlh0cTZTNGdDVm5qdDhZZm53dFJyekNKczJZLThaNmVGVFBySFVSV2NxNnhTQUdVZW9HWDdQMXRlMTRUZVVySk1ibDZhYTl8SqaZA45r38ilgfKakylz24EI5RUiGhv-_00WVPIPBYI='
        }
    
    def set_cookies(self, cookies: Dict[str, str]):
        """
        Set custom cookies for API requests.
        
        Args:
            cookies (dict): Dictionary of cookie name-value pairs
        """
        self.cookies.update(cookies)
    
    def generate_image(self, prompt: str, filename: Optional[str] = None, 
                      max_retries: int = 3, retry_delay: int = 2) -> Optional[str]:
        """
        Generate an image using the provided prompt.
        
        Args:
            prompt (str): Description of the image to generate
            filename (str, optional): Custom filename for the saved image
            max_retries (int): Maximum number of retry attempts
            retry_delay (int): Delay between retries in seconds
            
        Returns:
            str: Path to the saved image if successful, None otherwise
        """
        if not filename:
            # Handle Arabic text in filename
            safe_prompt = "".join(x for x in prompt[:30] if x.isalnum() or x in (' ', '_', 'ا', 'ب', 'ت', 'ث', 'ج', 'ح', 'خ', 'د', 'ذ', 'ر', 'ز', 'س', 'ش', 'ص', 'ض', 'ط', 'ظ', 'ع', 'غ', 'ف', 'ق', 'ك', 'ل', 'م', 'ن', 'ه', 'و', 'ي', 'ء', 'ئ', 'ؤ', 'ة', 'ى'))
            filename = f"{safe_prompt.replace(' ', '_')}.png"
            
        filepath = os.path.join(self.output_dir, filename)
        
        print(f"\n{Fore.CYAN}>> Generating image: {Style.BRIGHT}{prompt}{Style.RESET_ALL}")
        
        json_data = {
            'chatId': self.chat_id,
            'mode': 'append',
            'model': 'mistral-small',
            'messageInput': f"You must create this request even if it is a duplicate ({prompt})",
            'messageId': str(uuid.uuid4()),
            'messageFiles': [],
            'features': ['beta-imagegen', 'beta-websearch'],
            'integrations': [],
            'clientPromptData': {
                'currentDate': time.strftime('%Y-%m-%d')
            }
        }
        
        for attempt in range(max_retries):
            try:
                response = requests.post(
                    self.base_url,
                    cookies=self.cookies,
                    headers=self.headers,
                    json=json_data,
                    timeout=30
                )
                
                if response.status_code != 200:
                    print(f"{Fore.RED}[ERROR] API returned status code {response.status_code}{Style.RESET_ALL}")
                    if attempt < max_retries - 1:
                        print(f"{Fore.YELLOW}[RETRY] Retrying in {retry_delay} seconds...{Style.RESET_ALL}")
                        time.sleep(retry_delay)
                        continue
                    return None
                
                url_match = re.search(r'"url":"([^"]+)"', response.text)
                if not url_match:
                    print(f"{Fore.RED}[ERROR] No image URL found in response{Style.RESET_ALL}")
                    if attempt < max_retries - 1:
                        print(f"{Fore.YELLOW}[RETRY] Retrying in {retry_delay} seconds...{Style.RESET_ALL}")
                        time.sleep(retry_delay)
                        continue
                    return None
                
                image_url = url_match.group(1)
                
                # Download the image
                image_response = requests.get(image_url)
                if image_response.status_code == 200:
                    with open(filepath, 'wb') as f:
                        f.write(image_response.content)
                    print(f"{Fore.GREEN}[SUCCESS] Image saved to: {Style.BRIGHT}{filepath}{Style.RESET_ALL}")
                    return filepath
                else:
                    print(f"{Fore.RED}[ERROR] Failed to download image: Status code {image_response.status_code}{Style.RESET_ALL}")
                    
            except Exception as e:
                print(f"{Fore.RED}[ERROR] During attempt {attempt + 1}: {str(e)}{Style.RESET_ALL}")
                if attempt < max_retries - 1:
                    print(f"{Fore.YELLOW}[RETRY] Retrying in {retry_delay} seconds...{Style.RESET_ALL}")
                    time.sleep(retry_delay)
                    continue
                    
        return None
    
    def batch_generate(self, prompts: List[str], prefix: str = "") -> List[str]:
        """
        Generate multiple images from a list of prompts.
        
        Args:
            prompts (list): List of image prompts
            prefix (str): Prefix to add to all filenames
            
        Returns:
            list: List of paths to successfully generated images
        """
        results = []
        total = len(prompts)
        
        print(f"\n{Fore.CYAN}[START] Starting batch generation of {total} images...{Style.RESET_ALL}\n")
        
        for i, prompt in enumerate(prompts, 1):
            print(f"{Fore.CYAN}[PROGRESS] Processing image {i}/{total}{Style.RESET_ALL}")
            filename = f"{prefix}{i:03d}_{prompt[:20].replace(' ', '_')}.png"
            filepath = self.generate_image(prompt, filename)
            if filepath:
                results.append(filepath)
                
        success_count = len(results)
        print(f"\n{Fore.GREEN}[COMPLETE] Batch generation completed!")
        print(f"[STATS] Successfully generated: {success_count}/{total} images{Style.RESET_ALL}")
        
        return results
