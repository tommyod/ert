gen_kw_export_file = "parameters";

import jinja2
import json
import os
import yaml

#default export file name found in enkf_defaults.hpp
DEFAULT_GEN_KW_EXPORT_NAME = "parameters.json"

class TemplateRender:
    @staticmethod
    def load_data(filename):
        """Will try to load data from @filename first as yaml, and if that fails,
        as json. If both fail, a ValueError with both of the error messages will be
        raised.
        """
        with open(filename) as fin:
            try:
                return yaml.load(fin)
            except Exception as yaml_err:
                pass

            try:
                return json.load(fin)
            except Exception as json_err:
                pass

        err_msg = '%s is neither yaml (err_msg=%s) nor json (err_msg=%s)'
        raise IOError(err_msg % (filename, str(yaml_err), str(json_err)))
    @staticmethod
    def _load_template(template_path):
        path, filename = os.path.split(template_path)
        return jinja2.Environment(
            loader=jinja2.FileSystemLoader(path or './')
        ).get_template(filename)

    @staticmethod
    def _generate_file_namespace(filename):
        return os.path.splitext(os.path.basename(filename))[0]

    @staticmethod
    def _load_input(input_files):
        data = {}
        for input_file in input_files:
            input_namespace = TemplateRender._generate_file_namespace(input_file)
            data[input_namespace] = TemplateRender.load_data(input_file)

        return data

    @staticmethod
    def _assert_input(input_files, template_file, output_file):
        for input_file in input_files:
            if not os.path.isfile(input_file):
                raise ValueError('Input file: %s, does not exist..' % input_file)

        if not os.path.isfile(template_file):
            raise ValueError('Template file: %s, does not exist..' % template_file)

        if not isinstance(output_file, str):
            raise TypeError('Expected output path to be a string')

    @staticmethod
    def render_template(input_files, template_file, output_file):

        if isinstance(input_files, basestring) and input_files:
            input_files = [input_files,]

        all_input_files = [DEFAULT_GEN_KW_EXPORT_NAME,]
        if input_files:
            all_input_files += input_files


        TemplateRender._assert_input(all_input_files, template_file, output_file)

        template = TemplateRender._load_template(template_file)
        data = TemplateRender._load_input(all_input_files)
        with open(output_file, 'w') as fout:
            fout.write(template.render(**data))
