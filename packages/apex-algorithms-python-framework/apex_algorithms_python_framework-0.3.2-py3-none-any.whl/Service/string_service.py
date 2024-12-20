class StringService:
    def transform_to_camel_case(self, input_string: str) -> str:

        words = input_string.split('-')

        return ''.join(word.capitalize() for word in words)