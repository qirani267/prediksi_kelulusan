import numpy as np
import joblib

class Predict:
    def predict(umur, jenis_kelamin, domisili, status_sekolah, asal_sekolah, kegiatan_organisasi, penghasilan_ortu, ips1, ips2, ips3, ips4, ips5, ips6):
        try:
            return Predict.preprocessDataAndPredict(umur, jenis_kelamin, domisili, status_sekolah, asal_sekolah, kegiatan_organisasi, penghasilan_ortu, ips1, ips2, ips3, ips4, ips5, ips6)
        except ValueError:
            return "Please Enter valid values"

    def preprocessDataAndPredict(umur, jenis_kelamin, domisili, status_sekolah, asal_sekolah, kegiatan_organisasi, penghasilan_ortu, ips1, ips2, ips3, ips4, ips5, ips6):
        # keep all inputs in array
        test_data = [umur, jenis_kelamin, domisili, status_sekolah, asal_sekolah, 
        kegiatan_organisasi, penghasilan_ortu, ips1, ips2, ips3, ips4, ips5, ips6]
        print(test_data)

        # convert value data into numpy array
        test_data = np.array(test_data)

        # reshape array
        test_data = test_data.reshape(1, -1)
        print(test_data)

        # open file
        file = open("models/MODELBARU.pkl", "rb")

        # load trained model
        trained_model = joblib.load(file)

        # predict
        prediction = trained_model.predict(test_data)

        return prediction
