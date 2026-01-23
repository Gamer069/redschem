from dataclasses import dataclass, fields
from typing import Optional
from warnings import warn


@dataclass
class Header:
    title: str
    authors: list[str]
    description: str
    input: Optional[str] = None
    output: Optional[str] = None
    speed: Optional[str] = None
    notes: Optional[str] = None

    @staticmethod
    def parse(data: str):
        last_field = None
        kvs = {}
        key_map = {
            "author": "authors"
        }
        valid_fields = {f.name.lower(): f.name for f in fields(Header)}

        for line in data.splitlines():

            # continue if line is empty
            line = line.strip()
            if not line:
                continue

            # concat to last field if line doesn't contain :
            if ":" not in line and last_field is not None:
                if last_field == "authors":
                    kvs.setdefault("authors", []).extend([a.strip() for a in line.split(",")])
                else:
                    kvs[last_field] += " " + line
                continue

            k, v = line.split(":", 1)
            k = k.strip().lower()
            v = v.strip()

            # map to dataclass field, including author->authors
            field_name = key_map.get(k) or valid_fields.get(k)
            if field_name is None:
                warn("Invalid key in schematic header.")
                continue

            if field_name == "authors":
                kvs.setdefault("authors", []).extend([a.strip() for a in v.split(",")])
            else:
                kvs[field_name] = v

            last_field = field_name

        # fill missing fields
        for f in valid_fields.values():
            kvs.setdefault(f, None)
        kvs.setdefault("authors", [])

        return Header(**kvs)


@dataclass
class Schem:
    header: Header
    category: str
    subcategory: str
    schem: str
    image: str
    extra_data: Optional[str] = None

    async def add_to_db(self, db):
        await db.execute(
            """
                INSERT INTO schematics (
                    category,
                    subcategory,

                    image,
                    schem,

                    title,
                    authors,
                    description,

                    input,
                    output,
                    speed,

                    notes,
                    extra_data
                ) VALUES (
                    $1,
                    $2,
                    $3,
                    $4,
                    $5,
                    $6,
                    $7,
                    $8,
                    $9,
                    $10,
                    $11,
                    $12
                )
            """,
            self.category,
            self.subcategory,
            self.image,
            self.schem,
            self.header.title,
            self.header.authors,
            self.header.description,
            self.header.input,
            self.header.output,
            self.header.speed,
            self.header.notes,
            self.extra_data
        )
