from importlib.resources import path
from itertools import count
from turtle import color
from unittest import result
from flask import redirect, render_template, request, send_file, session
from matplotlib.pyplot import legend, subplot
from sqlalchemy import create_engine, null
from functions.predict import Predict
import pandas as pd
from matplotlib import pyplot as plt
import flask_excel as excel


def check_authentication():
    if not session.get("login_by_admin") is None:
        return True

def init(app, mysql):

    @app.route('/admin', methods=['GET'])
    def admin():
        if check_authentication() != True:
            return redirect('/')

        return render_template('admin/dashboard.html', active='admin')

    @app.route('/admin/data_mahasiswa', methods=['GET'])
    def data_mahasiswa():
        if check_authentication() != True:
            return redirect('/')

        con = mysql.connect()
        cursor = con.cursor()
        query = "SELECT * FROM mahasiswa"
        cursor.execute(query)
        rows = cursor.fetchall()
        cursor.close()

        return render_template('admin/data_mahasiswa.html', data=rows, active='admin/data_mahasiswa')

    @app.route('/admin/upload_excel', methods=['POST'])
    def import_mhs():
        if check_authentication() != True:
            return redirect('/')

        con = mysql.connect()
        cursor = con.cursor()

        query = "TRUNCATE prediksi.mahasiswa"
        cursor.execute(query)
        con.commit()
        
        df = pd.read_excel(request.files.get('file'))
        row = pd.DataFrame(df)
        count_row = df.shape[0]     

        # print(count_row)
        # print(row.iloc[0])

        for x in range(0, count_row):
            col = row.iloc[x]
            con = mysql.connect()
            cursor = con.cursor()

        # jenis kelamin
            if col[4] == "laki-laki":
                col4 = "0"
            else:
                col4 = "1"

        # domisili
            if col[5] == "pemalang":
                col5 = "3"
            elif col[5] == "brebes":
                col5 ="2"
            elif  col[5] == "tegal":
                col5 = "1"
            else:
                col5 = "-999"

        # status sekolah
            if col[6] == "negeri":
                col6 = "0"
            else:
                col6 = "1"

        # asal sekolah
            if col[7] == "sma":
                col7 = "0"
            else:
                col7 = "1"

        # kegiatan organisasi
            if col[8] == "tidak":
                col8 = "0"
            else:
                col8 = "1"

        # penghasilan ortu
            if col[9] == "tinggi":
                col9 = "2"
            elif col[9] == "sedang":
                col9 = "1"
            else:
                col9 = "0"

            query = "INSERT INTO `mahasiswa` (`id`, `nim`, `nama_lengkap`, `umur`, `jenis_kelamin`, `domisili`, `status_sekolah`, `asal_sekolah`, `kegiatan_organisasi`, `penghasilan_ortu`, `ips1`, `ips2`, `ips3`, `ips4`, `ips5`, `ips6`, `status_kelulusan`) VALUES (NULL, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, NULL);"
            cursor.execute(query, (col[1], col[2], col[3], col4, col5, col6, col7, col8, col9, col[10], col[11], col[12], col[13], col[14], col[15]))
            con.commit()

        return redirect('/admin/data_mahasiswa')

    # Tambah mahasiswa

    @app.route('/admin/tambah_mahasiswa', methods=['POST'])
    def tambah_mhs():
        if check_authentication() != True:
            return redirect('/')

        nama = request.form.get('nama')
        nim = request.form.get('nim')
        umur = request.form.get('umur')
        jenis_kelamin = request.form.get('jenis_kelamin')
        domisili = request.form.get('domisili')
        status_sekolah = request.form.get('status_sekolah')
        asal_sekolah = request.form.get('asal_sekolah')
        kegiatan_organisasi = request.form.get('kegiatan_organisasi')        
        penghasilan_ortu = request.form.get('penghasilan_ortu')
        ips1 = request.form.get('ips1')
        ips2 = request.form.get('ips2')
        ips3 = request.form.get('ips3')
        ips4 = request.form.get('ips4')
        ips5 = request.form.get('ips5')
        ips6 = request.form.get('ips6')

        con = mysql.connect()
        cursor = con.cursor()
        query = "INSERT INTO `mahasiswa` (`id`, `nim`, `nama_lengkap`, `umur`, `jenis_kelamin`, `domisili`, `status_sekolah`, `asal_sekolah`, `kegiatan_organisasi`, `penghasilan_ortu`, `ips1`, `ips2`, `ips3`, `ips4`, `ips5`, `ips6`, `status_kelulusan`) VALUES (NULL, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, NULL);"
        cursor.execute(query, (nim, nama, umur, jenis_kelamin, domisili, status_sekolah, asal_sekolah, kegiatan_organisasi, 
                                penghasilan_ortu, ips1, ips2, ips3, ips4, ips5, ips6))
        con.commit()

        return redirect('/admin/data_mahasiswa')

    # edit mahasiswa

    @app.route('/admin/edit_mhs/<nim>', methods=['GET'])
    def edit_mhs_s(nim):
        if check_authentication() != True:
            return redirect('/')

        con = mysql.connect()
        cursor = con.cursor()
        query = "SELECT * FROM mahasiswa WHERE nim=%s"
        cursor.execute(query, (nim))
        rows = cursor.fetchone()

        return render_template('admin/edit_mahasiswa.html', nama=rows[2], umur=rows[3], jenis_kelamin=rows[4], domisili=rows[5],
                               status_sekolah=rows[6], asal_sekolah=rows[7],kegiatan_organisasi=rows[8], penghasilan_ortu=rows[9], ips1=rows[10], ips2=rows[11], ips3=rows[12], ips4=rows[13], ips5=rows[14], nim=rows[1], ips6=rows[15], active='admin/data_mahasiswa')
    # edit 
    @app.route('/admin/edit_mhs', methods=['POST'])
    def edit_mhs():
        if check_authentication() != True:
            return redirect('/')

        con = mysql.connect()
        cursor = con.cursor()

        nama = request.form.get('nama')
        nim = request.form.get('nim')
        umur = request.form.get('umur')
        jenis_kelamin = request.form.get('jenis_kelamin')
        domisili = request.form.get('domisili')
        status_sekolah = request.form.get('status_sekolah')
        asal_sekolah = request.form.get('asal_sekolah')
        kegiatan_organisasi = request.form.get('kegiatan_organisasi')        
        penghasilan_ortu = request.form.get('penghasilan_ortu')
        ips1 = request.form.get('ips1')
        ips2 = request.form.get('ips2')
        ips3 = request.form.get('ips3')
        ips4 = request.form.get('ips4')
        ips5 = request.form.get('ips5')
        ips6 = request.form.get('ips6')

        query = "UPDATE mahasiswa SET nama_lengkap = %s, umur = %s, jenis_kelamin = %s, domisili = %s, status_sekolah = %s, asal_sekolah = %s, kegiatan_organisasi = %s, penghasilan_ortu = % s, ips1 = %s, ips2 = %s, ips3 = %s, ips4 = %s, ips5 = %s, ips6 = %s, status_kelulusan = %s WHERE nim = %s"
        cursor.execute(query, (nama, umur, jenis_kelamin, domisili, status_sekolah, asal_sekolah, kegiatan_organisasi, 
                                penghasilan_ortu, ips1, ips2, ips3, ips4, ips5, ips6, nim))
        con.commit()

        return redirect('/admin/data_mahasiswa')
# delete
    @app.route('/admin/del_mhs/<nim>', methods=['GET'])
    def del_mhs(nim):
        if check_authentication() != True:
            return redirect('/')

        con = mysql.connect()
        cursor = con.cursor()

        query = "DELETE FROM mahasiswa WHERE nim = %s"
        cursor.execute(query, (str(nim)))
        con.commit()

        return redirect('/admin/data_mahasiswa')

    @ app.route('/admin/prediksi', methods=['GET'])
    def prediksi():
        if check_authentication() != True:
            return redirect('/')

        con = mysql.connect()
        cursor = con.cursor()
        query = "SELECT * FROM mahasiswa"
        cursor.execute(query)
        rows = cursor.fetchall()
        cursor.close()

        return render_template('admin/prediksi.html', data=rows, active='admin/prediksi')

# Prediksi 
    @ app.route('/admin/prediksi', methods=['POST'])
    def manual_predict():
        if check_authentication() != True:
            return redirect('/')

        nama = request.form.get('nama')
        nim = request.form.get('nim')
        umur = request.form.get('umur')
        jenis_kelamin = request.form.get('jenis_kelamin')
        domisili = request.form.get('domisili')
        status_sekolah = request.form.get('status_sekolah')
        asal_sekolah = request.form.get('asal_sekolah')
        kegiatan_organisasi = request.form.get('kegiatan_organisasi')        
        penghasilan_ortu = request.form.get('penghasilan_ortu')
        ips1 = request.form.get('ips1')
        ips2 = request.form.get('ips2')
        ips3 = request.form.get('ips3')
        ips4 = request.form.get('ips4')
        ips5 = request.form.get('ips5')
        ips6 = request.form.get('ips6')

        hasil = str(Predict.predict(umur, jenis_kelamin, domisili, status_sekolah, asal_sekolah, kegiatan_organisasi, 
                                penghasilan_ortu, ips1, ips2, ips3, ips4, ips5, ips6)[0])

        return render_template('admin/hasil_prediksi.html', hasil=hasil, nama=nama, umur=umur, jenis_kelamin=jenis_kelamin, domisili=domisili, status_sekolah=status_sekolah,
                                asal_sekolah=asal_sekolah, kegiatan_organisasi=kegiatan_organisasi, penghasilan_ortu=penghasilan_ortu, ips1=ips1, ips2=ips2, ips3=ips3, ips4=ips4, ips5=ips5, nim=nim, ips6=ips6, active='admin/prediksi')

# Single Prediksi(manual prediksi)
    @ app.route('/admin/single_predict/<nim>', methods=['GET'])
    def single_predict(nim):
        if check_authentication() != True:
            return redirect('/')

        con = mysql.connect()
        cursor = con.cursor()
        query = "SELECT * FROM mahasiswa WHERE nim=%s"
        cursor.execute(query, (nim))
        rows = cursor.fetchone()

        hasil = str(Predict.predict(
            rows[3], rows[4], rows[5], rows[6], rows[7], rows[8], rows[9], rows[10], rows[11], rows[12], rows[13], rows[14], rows[15])[0])

        query = "UPDATE mahasiswa SET status_kelulusan = %s WHERE nim = %s"
        cursor.execute(query, (hasil, str(nim)))
        con.commit()

        return render_template('admin/hasil_prediksi.html', hasil=hasil, nama=rows[2], umur=rows[3], jenis_kelamin=rows[4], domisili=rows[5], 
                                status_sekolah=rows[6], asal_sekolah=rows[7], kegiatan_organisasi=rows[8], penghasilan_ortu=rows[9], ips1=rows[10], ips2=rows[11], ips3=rows[12], ips4=rows[13], ips5=rows[14], nim=rows[1], ips6=rows[15], active='admin/prediksi')

    @ app.route('/admin/multi_predict', methods=['GET'])
    def multi_predict():
        if check_authentication() != True:
            return redirect('/')

        con = mysql.connect()
        cursor = con.cursor()
        query = "SELECT * FROM mahasiswa"
        cursor.execute(query)
        rows = cursor.fetchall()
        cursor.close()

        for dt in rows:
            con = mysql.connect()
            cursor = con.cursor()
            hasil = str(Predict.predict(
                dt[3], dt[4], dt[5], dt[6], dt[7], dt[8], dt[9], dt[10], dt[11], dt[12], dt[13], dt[14], dt[15])[0])

            query = "UPDATE mahasiswa SET status_kelulusan = %s WHERE nim = %s"
            print(hasil)
            cursor.execute(query, (hasil, str(dt[1])))
            con.commit()

        return redirect("/admin/hasil_multi_predict")

    @ app.route('/admin/hasil_multi_predict', methods=['GET'])
    def hasil_multi_predict():
        if check_authentication() != True:
            return redirect('/')

        con = mysql.connect()
        cursor = con.cursor()
        query = "SELECT * FROM mahasiswa"
        cursor.execute(query)
        rows = cursor.fetchall()
        cursor.close()

        return render_template('/admin/hasil_multi_prediksi.html', data=rows, active='admin/prediksi')
    
    @ app.route('/admin/rekap')
    def rekap():

        con = mysql.connect()
        cursor = con.cursor()

        query = 'SELECT status_kelulusan FROM mahasiswa'
        cursor.execute(query)
        con.commit()
        baris = cursor.fetchall()
        df = pd.DataFrame(baris)
        print(df)
        df.columns = ['status_kelulusan']
        data = df.groupby('status_kelulusan').size().reset_index(name='jumlah')
        dat = pd.DataFrame(data.jumlah)
        my_labels = 'Lulus Tepat Waktu', 'Tidak Lulus Tepat Waktu'
        my_color = ['green', 'red']
        dat.plot(kind='pie', labels=my_labels, autopct='%1.1f%%',
                 colors=my_color, subplots=True, stacked=True, legend=False)
        # plt.rcParams["figure.figsize"] = [7.00, 3.50]
        # plt.rcParams["figure.autolayout"] = True
        # df.groupby('predict').size().reset_index(name='jumlah').plot(kind="bar", color=[
        #     'red', 'aqua', 'green', 'blue'], x='predict', y='jumlah', stacked=True, legend=False, ylim=(0, 25))
        plt.title('Hasil Seluruh Rekap Kelulusan Mahasiswa ')
        plt.ylabel("")
        plt.savefig('static/img/image.png')

        return render_template('/admin/rekap.html')
    
    @ app.route('/download')
    def download_file():
        p = "template_excel.xlsx"
        return send_file(p,as_attachment=True)



        

    





