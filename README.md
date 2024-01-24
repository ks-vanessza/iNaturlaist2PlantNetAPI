# iNaturlaist To Pl@ntNetAPI predicition

## 1) Run `extract_inaturalist_img.py`  to get the img source
To get prediction from Pl@ntAPI first we need the image link. 
- Refer to [iNaturalist API](https://api.inaturalist.org/v1/docs/#!/Observations/get_observations_id) for parameter settings
- Add your CSV with the following structure with `x` in the first column and the observation links below 
```
x
https://www.inaturalist.org/observations/185168630
https://www.inaturalist.org/observations/185168603
https://www.inaturalist.org/observations/185168585
https://www.inaturalist.org/observations/185168570
https://www.inaturalist.org/observations/185168542
```
*note: The CSV is loaded from `../Data_processing/df_inat.csv`*

## 2) Run `get_predicition.py` to get the predictions
- Add your API key
- Refer to [Pl@netAPI Documentation](https://my.plantnet.org/doc/openapi) for parameter settings