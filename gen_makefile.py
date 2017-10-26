#!/usr/bin/env python3
import os


def read_list(fin_name, fout_name, root_folder):
    with open(fin_name, 'r') as fin, open(fout_name, 'w') as fout:
        headers = next(fin).rstrip('\n').split('\t')
        assert headers == ['name', 'image_id', 'face_id',
                           'url', 'bbox', 'sha256']
        all_targets = []
        for line in fin:
            name, image_id, face_id, url, bbox, sha256 = line.rstrip('\n').split('\t')
            name = '_'.join(name.split(' '))
            folder = os.path.join(root_folder, name)
            filename = '_'.join(name.split(' ') + [face_id.zfill(6), image_id.zfill(6), sha256])
            filename = os.path.join(folder, filename)
            all_targets.append(filename)
            fout.write("""{filename}:
\t@mkdir -p {folder}
\t-wget -t 3 --timeout 5 -nc --quiet -O {filename} {url}

""".format(filename=filename, folder=folder, url=url))

        fout.write("""
.DEFAULT: all

all: {}
""".format(' '.join(all_targets)))


def main():
    read_list('facescrub_actors.txt', 'Makefile', 'data/actor')
    read_list('facescrub_actresses.txt', 'Makefile1', 'data/actress')


if __name__ == '__main__':
    main()
