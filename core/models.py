    @staticmethod
    def _sort_key(record: SvodkaRecord):

        return (
            record.model.lower(),
            record.garage_number.lower(),
        )


    @staticmethod
    def _remove_duplicates(
        records: list[SvodkaRecord],
    ) -> list[SvodkaRecord]:

        unique = {}

        for record in records:

            key = (
                record.garage_number.strip().lower(),
            )

            unique[key] = record

        return sorted(
            unique.values(),
            key=SvodkaLoader._sort_key,
        )


    def load_unique(
        self,
        date_string: str,
    ) -> list[SvodkaRecord]:
        """
        Загружает предыдущий день
        без повторов.
        """

        return self._remove_duplicates(
            self.load(date_string)
        )
