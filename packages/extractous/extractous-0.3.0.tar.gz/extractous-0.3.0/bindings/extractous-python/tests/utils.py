from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity as cosine_sim
from lxml import etree

def cosine_similarity(text1, text2):
    """Calculate the cosine similarity between two texts."""

    # Create the CountVectorizer and transform the texts into vectors
    vectorizer = CountVectorizer().fit_transform([text1, text2])
    vectors = vectorizer.toarray()

    # Calculate cosine similarity between the two vectors
    cos_sim = cosine_sim(vectors)
    return cos_sim[0][1]


# def read_to_string(reader):
#     """Read from stream to string."""
#     result = ""
#     b = reader.read(4096)
#     while len(b) > 0:
#         result += b.decode("utf-8")
#         b = reader.read(4096)
#     return result

def read_to_string(reader):
    """Read from stream to string."""
    utf8_string = []
    buffer = bytearray(4096)

    while True:
        bytes_read = reader.readinto(buffer)
        # If no more data, exit the loop
        if bytes_read == 0:
            break
        # Decode the valid portion of the buffer and append it to the result
        utf8_string.append(buffer[:bytes_read].decode('utf-8'))

    # Join all parts into a single string
    return ''.join(utf8_string)


def read_file_to_bytearray(file_path: str):
    """Read file to bytes array."""
    with open(file_path, 'rb') as file:
        file_content = bytearray(file.read())
    return file_content


def is_expected_metadata_contained(expected: dict, current: dict) -> bool:
    """
    Check if all keys in `expected` are present in `current` and have identical values.
    """
    for key, expected_values in expected.items():
        actual_values = current.get(key)
        if actual_values is None:
            print(f"\nexpected key = {key} not found !!")
            return False
        elif actual_values != expected_values:
            print(f"\nvalues for key = {key} differ!! expected = {expected_values} and actual = {actual_values}")
            return False
    return True


def calculate_similarity_percent(expected, current):
    matches = 0
    total = 0

    # Iterate over all keys in the 'expected' dictionary
    for key, value1 in expected.items():
        if key in current:
            total += 1
            if value1 == current[key]:
                matches += 1

    if total == 0:
        return 0.0

    # Return the similarity percentage
    return matches / total


def extract_body_text(xml: str) -> str:
    """
    Extracts and returns plain text content from the <body> section of an XML
    string.
    """
    try:
        parser = etree.XMLParser(recover=True)
        root = etree.fromstring(xml.encode(), parser=parser)
        ns= {"ns": "http://www.w3.org/1999/xhtml"}
        body = root.find(".//ns:body", namespaces=ns)
        if body is None:
            return ""
        return "\n".join(body.itertext()).strip()
    except ET.ParseError as e:
        raise ValueError(f"Invalid XML input: {e}")
