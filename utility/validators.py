

def file_extension_validator_wrapper(*valid_extensions):

    def validate_file_extension(value):
        import os
        from django.core.exceptions import ValidationError
        ext = os.path.splitext(value.name)[1]  # [0] returns path+filename
        if not ext.lower() in valid_extensions:
            if len(valid_extensions) == 1:
                message = 'تنها پسوند مجاز {} می‌باشد.'.format(valid_extensions[0])
            else:
                message = 'تنها می‌توانید فایل با با پسوند های {} را آپلود کنید.'.format(str(valid_extensions))
            raise ValidationError(message)
    return validate_file_extension
