from youtubeenhanced.enums import Subtitles
from yta_general_utils.programming.parameter_validator import PythonValidator
from yta_general_utils.file.checker import FileValidator
from yta_general_utils.file.filename import get_file_extension
from yta_general_utils.file.reader import FileReader
from datetime import timedelta

import xml.etree.ElementTree as ET
import re


class YoutubeVideoSubtitleElement:
    """
    Class that represents one subtitle element
    of a Youtube video. This element is usually
    a single word.

    Attention: the 'duration' time represents
    the time the element is shown as subtitle,
    not the time the element is spoken in the
    video.
    """
    text: str = None
    """
    The text of this subtitle line.
    """
    start_time: int = None
    """
    The start time moment (in ms) of this subtitle
    line in the corresponding video.
    """
    duration: int = None
    """
    The time this subtitle line is shown in the
    corresponding video. This is not the amount of
    time the element is being spoken in the video.
    """

    @property
    def end_time(self):
        """
        The end time (in ms) based on the sum of the
        'start_time' and the 'duration'.
        """
        return self.start_time + self.duration

    def __init__(self, text: str, start_time: int, duration: int):
        self.text = text
        self.start_time = start_time
        self.duration = duration

class YoutubeVideoSubtitles:
    """
    Class to represent a Youtube video subtitles,
    contaning all the subtitle lines.
    """
    filename: str = None
    """
    The source file name used to obtain the subtitles.
    """
    elements: list[YoutubeVideoSubtitleElement] = None
    """
    The list of all the youtube video subtitles file
    elements processed.
    """

    def __init__(self, filename: str):
        """
        Parse the provided 'filename' youtube video 
        subtitles file, processes it and detects all
        the subtitle elements.
        """
        if not PythonValidator.is_string(filename) or not FileValidator.is_file(filename):
            raise Exception('The provided "filename" is not a valid string or filename.')
        
        file_extension = get_file_extension(filename)

        if file_extension not in Subtitles.get_all_values():
            raise Exception(f'The provided "filename" has an extension that is not accepted by our system. Try one of these: {Subtitles.get_all_values_as_str()}')
        
        if file_extension == Subtitles.TYPE_SRV1.value:
            elements = _parse_srv1_file(filename)
        elif file_extension == Subtitles.TYPE_SRV2.value:
            elements = _parse_srv2_file(filename)
        elif file_extension == Subtitles.TYPE_SRV3.value:
            elements = _parse_srv3_file(filename)
        elif file_extension == Subtitles.TYPE_JSON3.value:
            elements = _parse_json3_file(filename)
        elif file_extension == Subtitles.TYPE_TTML.value:
            elements = _parse_ttml_file(filename)
        elif file_extension == Subtitles.TYPE_VTT.value:
            elements = _parse_vtt_file(filename)

        self.filename = filename
        self.elements = elements

__all__ = [
    'YoutubeVideoSubtitleElement',
    'YoutubeVideoSubtitles'
]
        
def _time_to_ms(time_str):
    time_obj = timedelta(hours=int(time_str[:2]), minutes=int(time_str[3:5]), seconds=int(time_str[6:8]), milliseconds=int(time_str[9:]))
    return int(time_obj.total_seconds() * 1000)

def _parse_srv1_file(filename: str):
    """
    Subtitles are in this format:

    0:00:00.000 --> 0:00:03.760
    Este es el primer subtítulo.
    """
    subtitles = []
    with open(filename, 'r') as file:
        content = file.read()
        
        subtitle_blocks = re.split(r'\n\n', content.strip())  # Dos saltos de línea entre subtítulos
        for block in subtitle_blocks:
            lines = block.splitlines()
            
            # First row is the time
            time_range = lines[0]
            start_time_str, end_time_str = time_range.split(' --> ')
            start_time = _time_to_ms(start_time_str)
            end_time = _time_to_ms(end_time_str)
            
            # Second line is the text
            text = ' '.join(lines[1:]).strip()
            
            subtitles.append(YoutubeVideoSubtitleElement(text, start_time, end_time))
    
    return subtitles

def _parse_srv2_file(filename: str):
    if not PythonValidator.is_string(filename) or not FileValidator.is_file(filename):
        raise Exception('The provided "filename" is not a valid string or filename.')
    
    tree_root = ET.parse(filename).getroot()

    subtitles = [
        YoutubeVideoSubtitleElement(
            text = text_element.text.strip() if text_element.text else '',
            start_time = int(text_element.get('t', 0)),
            duration = int(text_element.get('d', 0))
        ) for text_element in tree_root.findall('.//text')
    ]
    
    return subtitles

def _parse_srv3_file(filename: str):
    if not PythonValidator.is_string(filename) or not FileValidator.is_file(filename):
        raise Exception('The provided "filename" is not a valid string or filename.')
    
    tree_root = ET.parse(filename).getroot()

    subtitles = [
        YoutubeVideoSubtitleElement(
            text = text_element.text.strip() if text_element.text else '',
            start_time = int(text_element.get('start', 0)),
            duration = int(text_element.get('duration', 0))
        ) for text_element in tree_root.findall('.//text')
    ]

    return subtitles

def _parse_json3_file(filename: str):
    if not PythonValidator.is_string(filename) or not FileValidator.is_file(filename):
        raise Exception('The provided "filename" is not a valid string or filename.')

    json_data = FileReader.read_json(filename)

    subtitles = [
        YoutubeVideoSubtitleElement(
            text = ' '.join(segment['utf8'] for segment in event.get('segs', [])),
            start_time = event.get('tStartMs', 0),
            duration = event.get('dDurationMs', 0)
        ) for event in json_data.get('events', [])
    ]

    return subtitles

def _parse_vtt_file(filename: str):
    if not PythonValidator.is_string(filename) or not FileValidator.is_file(filename):
        raise Exception('The provided "filename" is not a valid string or filename.')
    
    content = FileReader.read(filename)

    def clean_text_tags(text: str):
        return re.sub(r'<[^>]+>', '', text).strip()
    
    # Remove comments, empty lines or headers
    content = content.strip()
    
    # Split the content in blocks according to time line
    subtitle_blocks = re.split(r'\n(?=\d{2}:\d{2}:\d{2}\.\d{3})', content)
    
    subtitles = []
    for block in subtitle_blocks:
        lines = block.splitlines()
        
        # First row is time
        time_range = lines[0].split(' --> ')
        start_time_str = time_range[0].strip()
        end_time_str = time_range[1].strip()
        
        start_time = _time_to_ms(start_time_str)
        end_time = _time_to_ms(end_time_str)
        duration = end_time - start_time
        
        # Next rows are the text
        text_segments = [line.strip() for line in lines[1:]]

        # Clean tags and unify
        full_text = ' '.join([clean_text_tags(text) for text in text_segments])
        
        subtitles.append(YoutubeVideoSubtitleElement(full_text, start_time, duration))
    
    return subtitles

def _parse_ttml_file(filename: str):
    tree_root = ET.parse(filename).getroot()

    # This is the namespace used in this kind of file
    namespace = {'tt': 'http://www.w3.org/ns/ttml'}

    # Look for paragraphs containing it
    subtitles = []
    for p in tree_root.findall('.//tt:body//tt:div//tt:p', namespace):
        start_time_str = p.get('begin')
        end_time_str = p.get('end')
        
        if start_time_str and end_time_str:
            start_time = _time_to_ms(start_time_str)
            end_time = _time_to_ms(end_time_str)
            duration = end_time - start_time

            text = ''.join(p.itertext()).strip()

            # Guardamos el subtítulo como un objeto
            subtitles.append(YoutubeVideoSubtitleElement(text, start_time, duration))
    
    return subtitles