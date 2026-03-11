CONFIG_FILE_PATH = "config.yaml"
PARAMS_FILE_PATH = "params.yaml"
SYSTEM_PROMPT = '''
Extract structured product data from the input.

Return ONLY valid JSON with this schema:

{
 "title": "short clean title",
 "category": "category name",
 "brand": "brand name",
 "description": "1 sentence product description",
 "details": "1 sentence key features"
}
Ensure the JSON is syntactically valid.
Do not add explanations or markdown.
'''
