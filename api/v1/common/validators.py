''' file contains common functions'''


def does_object_exist(list_, object_key, object_attr):
    ''' find out if an object exist'''
    object_list = list(
        filter(
            lambda object_dict: object_dict[object_key] == object_attr,
            list_))
    if object_list:
        return object_list
    return False


def question_quality(string1="", string2=""):
    '''check the quality of questions sent to the platform'''
    if len(string1.strip()) < 10:
        return 'Your question seems to be of low quality, ensure your title makes sense'
    if len(string1) > len(string2):
        return 'Ensure your description provides detail,it should not be shorter than title'
    if string1.isdigit() or string2.isdigit():
        return 'Your question cannot have a title with numbers only'
    if len(string2.split()) < 3:
        return 'Please space question body properly readership'
    if len(string1.split()) < 2:
        return 'Please space question title properly readership'


def content_quality(string_, content=None):
    if len(string_.strip()) < 10:
        return 'Your {} seems to be of low quality, ensure your it makes sense'.format(content)
    if string_.isdigit():
        return 'Your {} cannot be numbers only'.format(content)
    if len(string_.split()) < 2:
        return 'Please space your {} properly for readership'.format(content)
