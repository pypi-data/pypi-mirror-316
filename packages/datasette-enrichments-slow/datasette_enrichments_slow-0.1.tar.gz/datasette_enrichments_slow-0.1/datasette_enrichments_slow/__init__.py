import asyncio
from datasette_enrichments import Enrichment
from datasette import hookimpl
from wtforms import Form, FloatField


@hookimpl
def register_enrichments():
    return [SlowEnrichment()]


class SlowEnrichment(Enrichment):
    name = "Slow"
    slug = "slow"
    description = "An enrichment on a slow loop to help debug progress bars"
    batch_size = 1

    async def initialize(self, datasette, db, table, config):
        pass

    async def get_config_form(self, db, table):
        class ConfigForm(Form):
            delay = FloatField(
                "Delay (seconds)",
                description="How many seconds to delay for each row",
                default=0.1,
            )

        return ConfigForm

    async def enrich_batch(
        self,
        db,
        table,
        rows,
        pks,
        config,
    ):
        for row in rows:
            await asyncio.sleep(config["delay"])
