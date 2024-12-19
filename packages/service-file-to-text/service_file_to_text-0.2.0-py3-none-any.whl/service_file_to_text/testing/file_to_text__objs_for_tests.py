from service_file_to_text.fast_api.File_To_Text__Fast_API import File_To_Text__Fast_API

file_to_text__fast_api         = File_To_Text__Fast_API().setup()
file_to_text__fast_api__app    = file_to_text__fast_api.app()
file_to_text__fast_api__client = file_to_text__fast_api.client()