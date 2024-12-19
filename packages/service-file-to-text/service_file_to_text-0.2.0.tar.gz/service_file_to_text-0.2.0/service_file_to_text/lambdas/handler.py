from mangum                                              import Mangum
from osbot_utils.utils.Env                               import get_env
from service_file_to_text.fast_api.File_To_Text__Fast_API import File_To_Text__Fast_API

fast_api__file_to_text = File_To_Text__Fast_API().setup()
app                  = fast_api__file_to_text.app()
run                  = Mangum(app)

if __name__ == "__main__":                              # pragma: no cover
    import uvicorn
    port = get_env('PORT', 8080)
    uvicorn.run(app, host="0.0.0.0", port=port)