#!/usr/bin/env python3
"""
Writes utterances and metadata in PaQu format.
"""

from typing import Iterable

from corpus2alpino.abstracts import Writer, Target
from corpus2alpino.models import Document, Utterance

FILE_SUFFIX = '.txt'


class PaQuWriter(Writer):
    """
    Wrapper for writing the strings and metadata in PaQu Metadata format
    """

    def write(self, document: Document, target: Target):
        has_metadata = False
        for line in self.output_metadata_items(document.metadata):
            target.write(document, line + '\n', suffix=FILE_SUFFIX)
            has_metadata = True

        if has_metadata:
            target.write(document, '\n', suffix=FILE_SUFFIX)

        for line in self.output_utterances(document.utterances, document.metadata):
            target.write(document, line, suffix=FILE_SUFFIX)

    def output_utterances(self, utterances: Iterable[Utterance], doc_metadata):
        """
        Passthrough input.
        """

        prev_metadata = {**doc_metadata}

        for utterance in utterances:
            metadata_display = '\n'.join(self.output_metadata_items(
                utterance.metadata, prev_metadata)) + '\n' if utterance.metadata else ''
            yield f'{metadata_display}{utterance.id}|{utterance.text}\n\n'

    def output_metadata_items(self, metadata, prev_metadata=None):
        for key, item in metadata.items():
            if prev_metadata == None or not key in prev_metadata or \
                    prev_metadata[key].value != item.value:
                yield f'##META {item.type} {key} = {item.value}'

        if prev_metadata != None:
            prev_metadata.clear()
            prev_metadata.update(metadata)
