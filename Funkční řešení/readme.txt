### Datasety - téma: Automotive

## CIS_Automotive_Kaggle_Sample
https://www.kaggle.com/datasets/cisautomotiveapi/large-car-dataset


## CAR
https://deepvisualmarketing.github.io/

 
Wolt
https://www.kaggle.com/datasets/muhammadwajeeharif/wolt-delivery-dataset
https://github.com/dmuiruri/woltorders





# vytvoř venv ve složce .venv
python3 -m venv .venv

# aktivuj ho
source .venv/bin/activate

# nainstaluj pandas (už to půjde)
pip install pandas


python clean_and_crop_data.py

deactivate


identifikatory:
Adv_ID, Genmodel_ID 


docker compose exec router01 mongosh -u martin -p rampouch --authenticationDatabase admin
