"""Simple demonstration dataset for Cihai."""

import typing as t

if t.TYPE_CHECKING:
    from cihai.types import UntypedDict

    class CharData(t.TypedDict, total=False):
        """Character definition dictionary."""

        definition: str

    Response = dict[str, CharData]


class DatasetExample:
    """Sample dataset to demonstrate a simple extension with Cihai.

    This object is passed into :meth:`cihai.Cihai.use` in the
    :class:`cihai.Cihai` object.
    """

    def get(self, request: str, response: "Response") -> "Response":
        """Return chinese character data from sample dataset.

        The source of information in this example is a :obj:`dict`. In real
        modules, the dataset may be a CSV, sqlite database, or an API. As long
        as the data appends to the :param:`response` and returns it.

        Parameters
        ----------
        request : str
            The character or string being looked up, e.g. '好'.

        Returns
        -------
        str
           Cihai response dictionary
        """
        dataset: Response = {"好": {"definition": "hao"}}

        if request in dataset:
            response[request] = response.get(request, {})
            response[request].update(dataset[request])

        return response

    def reverse(self, request: str, response: "Response") -> "Response":
        """Return chinese character data from a reverse lookup sample dataset.

        Parameters
        ----------
        request : str
            The character or string being looked up, e.g. '好'.

        Returns
        -------
        dict

            Cihai reverse look up. The results should be formatted as::

                {
                    '好': {
                        'definition': 'good.'
                    }
                }

            When the character already exists in :param:`response`, the character
            ``好`` must be mixed-in with, not overwritten.
        """
        dataset: Response = {"好": {"definition": "hao"}}

        for char in dataset:
            for val in dataset[char].values():
                assert isinstance(val, dict)
                if request in val:
                    if char not in dataset:
                        dataset[char] = {}
                    response[char].update(dataset[char])

        return response
