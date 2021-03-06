import pandas as pd
import trackintel as ti

import trackintel.visualization.staypoints
import trackintel.visualization.places


@pd.api.extensions.register_dataframe_accessor("as_places")
class PlacesAccessor(object):
    """A pandas accessor to treat (Geo)DataFrames as collections of places. This
    will define certain methods and accessors, as well as make sure that the DataFrame
    adheres to some requirements.

    Requires at least the following columns: 
    ``['user_id', 'geom']``

    Examples
    --------
    >>> df.as_places.plot()
    """

    required_columns = ['user_id', 'geom']

    def __init__(self, pandas_obj):
        self._validate(pandas_obj)
        self._obj = pandas_obj

    @staticmethod
    def _validate(obj):
        if any([c not in obj.columns for c in PlacesAccessor.required_columns]):
            raise AttributeError("To process a DataFrame as a collection of staypoints, " \
                + "it must have the properties [%s], but it has [%s]." \
                % (', '.join(PlacesAccessor.required_columns), ', '.join(obj.columns)))
        if obj.shape[0] > 0 and obj['geom'].geom_type[0] is not 'Point':
            raise AttributeError("The geometry must be a Point (only first checked).")

    def plot(self, *args, **kwargs):
        """Plots this collection of places. 
        See :func:`trackintel.visualization.places.plot_places`."""
        ti.visualization.places.plot_places(self._obj, *args, **kwargs)