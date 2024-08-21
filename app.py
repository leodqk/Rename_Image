from flask import Flask, render_template, request, redirect, url_for
import os

app = Flask(__name__)

# Thư mục chứa các thư mục exp
BASE_IMAGE_FOLDER = 'static'
app.config['BASE_IMAGE_FOLDER'] = BASE_IMAGE_FOLDER

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
        if 'select_exp' in request.form:
            selected_exp = request.form.get('exp')
            return redirect(url_for('index', exp=selected_exp))

        selected_exp = request.form.get('exp')
        if 'delete' in request.form:
            filename_to_delete = request.form['delete']
            file_path_to_delete = os.path.join(BASE_IMAGE_FOLDER, selected_exp, 'crops/person', filename_to_delete)
            if os.path.exists(file_path_to_delete):
                os.remove(file_path_to_delete)
            return redirect(url_for('index', exp=selected_exp))

        # Đổi tên ảnh
        filenames = request.form.getlist('filename')
        labels = request.form.getlist('label')

        # Đếm ID cho mỗi nhãn
        label_counters = {label: 1 for label in LABEL_MAPPING.values()}

        # Đổi tên ảnh
        for i in range(len(filenames)):
            old_path = os.path.join(BASE_IMAGE_FOLDER, selected_exp, 'crops/person', filenames[i])
            label = LABEL_MAPPING[labels[i]]
            new_filename = f"{label_counters[label]}_{label}.jpg"
            new_path = os.path.join(BASE_IMAGE_FOLDER, selected_exp, 'crops/person', new_filename)
            os.rename(old_path, new_path)
            label_counters[label] += 1  # Tăng ID cho nhãn đó

        return redirect(url_for('index', exp=selected_exp))

    # Đọc các thư mục exp từ thư mục gốc
    exps = [d for d in os.listdir(BASE_IMAGE_FOLDER) if os.path.isdir(os.path.join(BASE_IMAGE_FOLDER, d))]
    
    # Sắp xếp các thư mục exp theo thứ tự tăng dần
    exps.sort(key=lambda x: int(x.replace('exp', '')) if x.startswith('exp') and x[3:].isdigit() else 0)

    selected_exp = request.args.get('exp', exps[0] if exps else None)

    if selected_exp:
        images = os.listdir(os.path.join(BASE_IMAGE_FOLDER, selected_exp, 'crops/person'))
    else:
        images = []

    return render_template('index.html', exps=exps, current_exp=selected_exp, images=images, label_mapping=LABEL_MAPPING)

if __name__ == '__main__':
    app.run(debug=True)
