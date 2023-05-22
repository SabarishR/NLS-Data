# To activate the python environment
source E:/ML_APIs/Python_Environment/python3.8.10_kollectcall/Scripts/activate
# To navigate to project directory
cd E:/ML_APIs/API/TeraKollect_call_preferredSessionV1
# To set the environment variables
source config/config.sh
# To run python application as background process
nohup python Kollect_preferredSession_app.py &
# Successful deployment
echo "ML Application deployed Successfully"
# To wait terminal for 5 sec
sleep 5s
# To logout and close the terminal
logout
