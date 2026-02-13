"""MetaData model -- project metadata (title, artist, etc.)."""

from lxml import etree as ET


class MetaData:
    """Metadata for a DAWproject file.

    Attributes:
        title: Track/project title.
        artist: Artist name.
        album: Album name.
        original_artist: Original artist.
        composer: Composer.
        songwriter: Songwriter.
        producer: Producer.
        arranger: Arranger.
        year: Year of production.
        genre: Genre.
        copyright: Copyright notice.
        website: Website URL.
        comment: Additional comments.
    """

    def __init__(
        self,
        title=None,
        artist=None,
        album=None,
        original_artist=None,
        composer=None,
        songwriter=None,
        producer=None,
        arranger=None,
        year=None,
        genre=None,
        copyright=None,
        website=None,
        comment=None,
    ):
        self.title = title
        self.artist = artist
        self.album = album
        self.original_artist = original_artist
        self.composer = composer
        self.songwriter = songwriter
        self.producer = producer
        self.arranger = arranger
        self.year = year
        self.genre = genre
        self.copyright = copyright
        self.website = website
        self.comment = comment

    def to_xml(self):
        root = ET.Element("MetaData")

        fields = [
            ("Title", self.title),
            ("Artist", self.artist),
            ("Album", self.album),
            ("OriginalArtist", self.original_artist),
            ("Composer", self.composer),
            ("Songwriter", self.songwriter),
            ("Producer", self.producer),
            ("Arranger", self.arranger),
            ("Year", self.year),
            ("Genre", self.genre),
            ("Copyright", self.copyright),
            ("Website", self.website),
            ("Comment", self.comment),
        ]

        for tag, value in fields:
            if value is not None:
                elem = ET.SubElement(root, tag)
                elem.text = str(value)

        return root

    @classmethod
    def from_xml(cls, element):
        if element is None:
            return cls()
        return cls(
            title=element.findtext("Title"),
            artist=element.findtext("Artist"),
            album=element.findtext("Album"),
            original_artist=element.findtext("OriginalArtist"),
            composer=element.findtext("Composer"),
            songwriter=element.findtext("Songwriter"),
            producer=element.findtext("Producer"),
            arranger=element.findtext("Arranger"),
            year=element.findtext("Year"),
            genre=element.findtext("Genre"),
            copyright=element.findtext("Copyright"),
            website=element.findtext("Website"),
            comment=element.findtext("Comment"),
        )
