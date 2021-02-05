import os
from datetime import date, time
from unidecode import unidecode
from pydocx import PyDocX
from helpers.html2text import html2text
from data.document.template.keys.k2020 import header_keys, body_keys, footer_keys
from data.document.template.keys.k2020 import headers_colm, body_colm, footer_colm


class DocumentTool():

    """DocumentTool: Manipulacion de documentos 'Actas de compromiso'."""
    __author__ = "Grimpoteuthis (jphenao979@misena.edu.co)"
    __contributors__ = ["Nelson Andres Tique", "natique03@misena.edu.co"]

    # TODO:
    # Cambiar forma de acceder al archivo para evitar el uso de rutas
    # Permitir la creacion dinamica de formatos a partir archivo .docx

    # List with document sections - [header, body, footer]
    document_content = {}

    # path: string - docx path
    # outname: string - filename
    def docx_to_html(self, path, outname):
        with open(outname, "w") as file_html:
            html = PyDocX.to_html(path)
            file_html.write(html)
            return html

    # path: string - html path
    def read_html(self, path):
        with open(path, "r") as file_html:
            string_data = file_html.read()
            return string_data

    # html_data : string - html string
    def html_to_text(self, html_data):
        # html to plain text with markdown format
        text_data = html2text(html_data)
        split_data = self.del_space(text_data)
        split_data[0] = split_data[0] + split_data[1]
        del split_data[1]
        # index list of '' elements
        index_space = []
        for s in range(len(split_data)):
            if split_data[s] == '':
                index_space.append(s)
        index_space = sorted(index_space, reverse=True)
        for d in index_space:
            del split_data[d]
        return split_data

    # html_format : string - html path
    def html_to_string(self, html_format):
        html_data = self.read_html(html_format)
        split_html = self.del_space(html_data)
        sep = ''
        split_data = sep.join(split_html)
        return split_data

    # opt : string - template option
    def template_selector(self, opt):
        if opt == 2:
            template = 'data/document/template/string/2021.txt'
            return template
        else:
            template = 'data/document/template/string/2020.txt'
            return template

    # data_string : string - data
    def del_space(self, data_string):
        # Split with '\n'
        split_data = data_string.split('\n')
        for i in range(len(split_data)):
            # Delete spaces at the beginning and end of each string 
            split_data[i] = split_data[i].strip()
        return split_data

    # content : string - html data
    def get_content_data(self, content):
        text_data = self.html_to_text(content)
        header = self.extract_header_data(text_data)
        body_index = header['len_header']
        body = self.extract_body_data_v1(text_data[body_index:len(text_data)])
        footer_index = body_index + body[len(body)-1]
        footer = self.extract_footer_data(
            text_data[footer_index:len(text_data)])
        self.document_content = {
            'header': header,
            'body': body,
            'footer': footer
        }
        return self.document_content

    # content : list - html text
    # header_keys : list - dict keys
    def extract_header_data(self, content, header_keys=header_keys):
        header_content = {}
        k = 0
        cont = 0
        for i in range(len(content)):
            if cont == len(headers_colm):
                # header length in content
                header_content['len_header'] = k
                return header_content
            # Unicode to ASCII
            header_col = unidecode(content[k].lower())
            # check first index
            if headers_colm[0] in header_col:
                cont += 1
                header_content[header_keys[0]] = content[0]
                k += 1
            # check last index
            elif headers_colm[len(headers_colm)-1] in header_col:
                cont += 1
                header_content[header_keys[len(header_keys)-1]] = content[k]
                k += 1
            else:
                if headers_colm[i] in header_col:
                    cont += 1
                    header_content[header_keys[i]] = content[k+1]
                    k += 2

    # content : list - html text
    def extract_body_data_v1(self, content):
        body_content = []
        cont = 0
        for i in range(len(content)):
            body_col = unidecode(content[i].lower())
            if body_colm[len(body_colm)-1] in body_col:
                cont += 2
                body_content.append(content[i])
                body_content.append(cont)
                return body_content
            body_content.append(content[i])
            cont += 1

    # content : list - html text
    # body_keys : list - dict keys
    def extract_body_data_v2(self, content, body_keys=body_keys):
        body_content = {}
        cont = 0
        for i in range(len(content)):
            body_col = unidecode(content[i].lower())
            # check keys before and after the value
            if body_colm[i] in body_col and content[i+1] != body_colm[i+1]:
                # check first index
                if body_colm[0] in body_col[i]:
                    cont += 1
                    body_content[body_keys[0]] = content[i+1]
                # check last index
                elif body_colm[5] in body_col[i]:
                    cont += 1
                    body_content[body_keys[2]] = content[i+1]
                    return body_content
                else:
                    # Instructor data
                    pass

    # content : list - html text
    # footer_keys : list - dict keys
    def extract_footer_data(self, content, footer_keys=footer_keys):
        footer_content = {}
        user = {}
        list_user = []
        footer_col = ''
        cont = 6
        for i in range(len(content)):
            footer_col = unidecode(content[i].lower())
            # data before attendance 
            if footer_colm[1] in footer_col:
                footer_content[footer_keys[i]] = content[i+3]
            elif footer_colm[2] in footer_col:
                footer_content[footer_keys[i]] = content[i+3]
            elif footer_colm[3] in footer_col:
                footer_content[footer_keys[i]] = content[i+3]
            elif footer_colm[5] in footer_col:
                footer_content[footer_keys[3]] = content[i]
                footer_content[footer_keys[4]] = content[i+1] + content[i+2]
                footer_content[footer_keys[5]] = content[i+4]
            elif footer_colm[len(footer_colm)-1] in footer_col:
                # attendance
                for m in range(i+1, len(content)):
                    user[footer_keys[cont]] = content[m]
                    cont += 1
                    if cont == 13:
                        list_user.append(user)
                        user = {}
                        cont = 6
                footer_content['list_asis'] = list_user
                return footer_content
