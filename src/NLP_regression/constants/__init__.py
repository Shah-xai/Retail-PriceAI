CONFIG_FILE_PATH = "config.yaml"
PARAMS_FILE_PATH = "params.yaml"
SYSTEM_PROMPT = '''
Create a concise description of a product. Respond only in this format. Do not include part numbers.
 "title": "short clean title",
 "category": "category name",
 "brand": "brand name",
 "description": "1 sentence product description",
 "details": "1 sentence key features"
Rules:
- Return only the object
- No markdown
- No prose
- No comments
- No extra keys
- Never omit braces
'''
