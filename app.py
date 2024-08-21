from flask import Flask, render_template, request, redirect, url_for
import os

app = Flask(__name__)

# Thư mục chứa ảnh
IMAGE_FOLDER = 'static/person'
app.config['IMAGE_FOLDER'] = IMAGE_FOLDER

# Mapping từ các option sang nhãn
LABEL_MAPPING = {
    'F': 'focusing',
    'UF': 'unfocusing',
    'S': 'sleeping',
    'U': 'using_phone',
    'D': 'delete',
    'T': 'talking'
}

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Kiểm tra nếu có yêu cầu delete
        if 'delete' in request.form:
            filename_to_delete = request.form['delete']
            file_path_to_delete = os.path.join(IMAGE_FOLDER, filename_to_delete)
            if os.path.exists(file_path_to_delete):
                os.remove(file_path_to_delete)
            return redirect(url_for('index'))

        # Lấy danh sách file ảnh, nhãn mới và tên mới
        filenames = request.form.getlist('filename')
        labels = request.form.getlist('label')

        # Đếm ID cho mỗi nhãn
        label_counters = {label: 1 for label in LABEL_MAPPING.values()}

        # Đổi tên ảnh
        for i in range(len(filenames)):
            old_path = os.path.join(IMAGE_FOLDER, filenames[i])
            label = LABEL_MAPPING[labels[i]]
            new_filename = f"{label_counters[label]}_{label}.jpg"
            new_path = os.path.join(IMAGE_FOLDER, new_filename)
            os.rename(old_path, new_path)
            label_counters[label] += 1  # Tăng ID cho nhãn đó

        return redirect(url_for('index'))

    # Đọc các file ảnh từ thư mục
    images = os.listdir(IMAGE_FOLDER)
    return render_template('index.html', images=images, label_mapping=LABEL_MAPPING)

if __name__ == '__main__':
    app.run(debug=True)
