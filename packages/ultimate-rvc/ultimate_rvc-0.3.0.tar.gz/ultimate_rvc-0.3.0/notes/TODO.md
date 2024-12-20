# TODO

* add support for downloading custom pretrained models (for training)
  * must look in applio repo not rvc-cli repo
* add support for extracting f0 curve file from audio track 
  * must look in applio repo not rvc-cli repo
  * with f0  curves files can then test the custom f0 curve file parameter for voice conversion
* add support for blending voice models
* add support for getting model information
* add support for getting audio information
* upgrade audio-separator to latest version
  * then also update documentation as downloading diffq manually is no longer needed on windows
* upgrade gradio to latest
  * also remove gradio stub files as they are no longer needed
  * but then need to make updates to gradio imports in web package
* synchronize rvc backend package with latest changes from rvc-cli
* support more input files for tts than just .txt
* support other initial tts models than just edge tts
* fix new problem with hot reload:

  ```python
  Reloading src.ultimate_rvc.web.main failed with the following exception: 
  Traceback (most recent call last):
    File "C:\Users\Jacki\repositories\ultimate-rvc\uv\.venv\Lib\site-packages\gradio\utils.py", line 302, in watchfn
      changed_module = _find_module(changed)
                      ^^^^^^^^^^^^^^^^^^^^^
    File "C:\Users\Jacki\repositories\ultimate-rvc\uv\.venv\Lib\site-packages\gradio\utils.py", line 226, in _find_module
      for s, v in sys.modules.items():
                  ^^^^^^^^^^^^^^^^^^^
  RuntimeError: dictionary changed size during iteration
  ```


* should rename instances of "models" to "voice models"
* make subsections under accorditions under one click generation tab into sub accordions ?
  * applies for voice conversion options and audio mixing options
* fix problem with audio components restarting if play button is pressed too fast after loading new audio
  * this is a gradio bug so report?

* need to consider consolidating the commands exposed main.py, song_cover.py and tts.py under ultimate_rvc.cli.generate into just one generate command.

## Project/task management

* Should find tool for project/task management
* Tool should support:
  * hierarchical tasks
  * custom labels and or priorities on tasks
  * being able to filter tasks based on those labels
  * being able to close and resolve tasks
  * Being able to integrate with vscode
  * Access for multiple people (in a team)
* Should migrate the content of this file into tool
* Potential candidates
  * GitHub projects
    * Does not yet support hierarchical tasks so no
  * Trello
    * Does not seem to support hierarchical tasks either
  * Notion
    * Seems to support hierarchical tasks, but is complicated
  * Todoist
    * seems to support both hierarchical tasks, custom labels, filtering on those labels, multiple users and there are unofficial plugins for vscode.

## Front end

### Modularization

* Improve modularization of web code using helper functions defined [here](https://huggingface.co/spaces/WoWoWoWololo/wrapping-layouts/blob/main/app.py)
* Split front-end modules into further sub-modules.
  * Structure of web folder should be:
    * `web`
      * `manage_models`
        * `__init__.py`
        * `main.py`
      * `manage_audio`
        * `__init__.py`
        * `main.py`
      * `generate_song_covers`
        * `__init__.py`
        * `main.py`
        * `one_click_generation`
          * `__init__.py`
          * `main.py`
          * `accordions`
            * `__init__.py`
            * `options_x.py` ... ?
        * `multi_step_generation`
          * `__init__.py`
          * `main.py`
          * `accordions`
            * `__init__.py`
            * `step_X.py` ...
      * `common.py`
    * For `multi_step_generation/step_X.py`, its potential render function might have to take the set of all "input tracks" in the multi-step generation tab, so these will then have to be defined in `multi_step_generation/main.py`. Other components passed to `multi_step_generation/main.py` might also need to be passed further down to `multi_step_generation/step_X.py`
    * For `one_click_generation/option_X.py`, its potential render function should
        render the accordion for the given options and return the components defined in the accordion? Other components passed to `one_click_generation/main.py` might also need to be passed further down to `one_click_generation/option_X.py`
  * Import components instead of passing them as inputs to render functions (DIFFICULT TO IMPLEMENT)
    * We have had problems before with component ids when components are instantiated outside a Blocks context in a separate module and then import into other modules and rendered in their blocks contexts.

### Multi-step generation

* If possible merge two consecutive event listeners using `update_cached_songs` in the song retrieval accordion.
* add description describing how to use each accordion and suggestions for workflows

* add option for adding more input tracks to the mix song step
  * new components should be created dynamically based on a textfield with names and a button for creating new component
  * when creating a new component a new transfer button and dropdown should also be created
  * and the transfer choices for all dropdowns should be updated to also include the new input track
  * we need to consider how to want to handle vertical space
    * should be we make a new row once more than 3 tracks are on one row?
      * yes and there should be also created the new slider on a new row
      * right under the first row (which itself is under the row with song dir dropdown)

* should also have the possiblity to add more tracks to the pitch shift accordion.

* add a confirmation box with warning if trying to transfer output track to input track that is not empty.
  * could also have the possibility to ask the user to transfer to create a new input track and transfer the output track to it.
  * this would just be the same pop up confirmation box as before but in addition to yes and cancel options it will also have a "transfer to new input track" option.
  * we need custom javasctip for this.

### Common

* save default values for options for song generation in an `SongCoverOptionDefault` enum.
  * then reference this enum across the two tabs
  * and also use `list[SongCoverOptionDefault]` as input to reset settings click event listener in single click generation tab.
* Persist state of app (currently selected settings etc.) across re-renders
  * This includes:
    * refreshing a browser windows
    * Opening app in new browser window
    * Maybe it should also include when app is started anew?
  * Possible solutions
    * use gr.browserstate to allow state to be preserved acrross page loads.
    * Save any changes to components to a session dictionary and load from it upon refresh
      * See [here](https://github.com/gradio-app/gradio/issues/3106#issuecomment-1694704623)
      * Problem is that this solution might not work with accordions or other types of blocks
            * should use .expand() and .collapse() event listeners on accordions to programmatically reset the state of accordions to what they were before after user has refreshed the page
    * Use localstorage
      * see [here](https://huggingface.co/spaces/YiXinCoding/gradio-chat-history/blob/main/app.py) and [here](https://huggingface.co/spaces/radames/gradio_window_localStorage/blob/main/app.py)

    * Whenever the state of a component is changed save the new state to a custom JSON file.
      * Then whenever the app is refreshed load the current state of components from the JSON file
      * This solution should probably work for Block types that are not components
* fix gradio problem where last field components on a row are not aligned (DIFFICULT TO IMPLEMENT)
  * current solution with manual `<br>` padding is way too hacky.
  * this is a gradio bug so report?
* need to fix the `INFO: Could not find files for the given pattern(s)` on startup of web application on windows (DIFFICULT TO IMPLEMENT)
  * this is an error that gradio needs to fix
* Remove reset button on slider components (DIFFICULT TO IMPLEMENT)
  * this is a gradio feature that needs to be removed.
* Fix that gradio removes special symbols from audio paths when loaded into audio components (DIFFICULT TO IMPLEMENT)
  * includes parenthesis, question marks, etc.
  * its a gradio bug so report?
* Add button for cancelling any currently running jobs (DIFFICULT TO IMPLEMENT)
  * Not supported by Gradio natively
  * Also difficult to implement manually as Gradio seems to be running called backend functions in thread environments
* dont show error upon missing confirmation (DIFFICULT TO IMPLEMENT)
  * can return `gr.update()`instead of raising an error in relevant event listener function
  * but problem is that subsequent steps will still be executed in this case
* clearing temporary files with the `delete_cache` parameter only seems to work if all windows are closed before closing the app process (DIFFICULT TO IMPLEMENT)
  * this is a gradio bug so report?

## Online hosting optimization

* make concurrency_id and concurrency limit on components be dependent on whether gpu is used or not
  * if only cpu then there should be no limit
* increase value of `default_concurrency_limit` in `Block.queue` so that the same event listener
  * can be called multiple times concurrently
* use `Block.launch()` with `max_file_size` to prevent too large uploads
* define as many functions with async as possible to increase responsiveness of app
  * and then use `Block.launch()` with `max_threads`set to an appropriate value representing the number of concurrent threads that can be run on the server (default is 40)
* Persist state of app (currently selected settings etc.) across re-renders
* consider setting `max_size` in `Block.queue()` to explicitly limit the number of people that can be in the queue at the same time
* clearing of temporary files should happen after a user logs in and out
  * and in this case it should only be temporary files for the active user that are cleared
    * Is that even possible to control?
* enable server side rendering (requires installing node and setting ssr_mode = true in .launch) (DIFFICULT TO IMPLEMENT)
  * Also needs to set GRADIO_NODE_PATH to point to the node executable
  * problem is that on windows there is a ERR_UNSUPPORTED_ESM_URL_SCHEME which needs to be fixed by gradio
    * see here <https://github.com/nodejs/node/issues/31710>
  * on linux it works but it is not possible to shutdown server using CTRL+ C

## Back end

### `generate_song_cover.py`

* intermediate file prefixes should be made into enums
* find framework for caching intermediate results rather than relying on your homemade system

  * Joblib: <https://medium.com/@yuxuzi/unlocking-efficiency-in-machine-learning-projects-with-joblib-a-python-pipeline-powerhouse-feb0ebfdf4df>
  * scikit learn: <https://scikit-learn.org/stable/modules/compose.html#pipeline>

  * <https://softwarepatternslexicon.com/machine-learning/infrastructure-and-scalability/workflow-management/pipeline-caching/>
  * <https://github.com/bmabey/provenance>
  * <https://docs.sweep.dev/blogs/file-cache>

* Support specific audio formats for intermediate audio file?
  * it might require some more code to support custom output format for all pipeline functions.

* expand `_get_model_name` so that it can take any audio file in an intermediate audio folder as input (DIFFICULT TO IMPLEMENT)
  * Function should then try to recursively
    * look for a corresponding json metadata file
    * find the model name in that file if it exists
    * otherwise find the path in the input field in the metadata file
    * repeat
  * should also consider whether input audio file belongs to step before audio conversion step
* use pydantic models to constrain numeric inputs (DIFFICULT TO IMPLEMENT)
  * for inputs to `convert` function for example
  * Use `Annotated[basic type, Field[constraint]]` syntax along with a @validate_call decorator on functions
  * Problem is that pyright does not support `Annotated` so we would have to switch to mypy
  
### `manage_models.py`

* use pandas.read_json to load public models table (DIFFICULT TO IMPLEMENT)

## CLI

### general

* look into typer replacement like cyclopts
  * so that we dont have to define separate cli wrappers for each function
  * just need to make sure that cyclopts can also do some of the automatic input validation that typer does

* replace _validate_exist and _validate_exists with _validate_provided. We dont need in the code to check whether the input exists as that is done by cli wrapper and gradio respectively. only exception is that we still need to check that model dir exists when given a model name

* fix problem with not being able to rename default "Options" panel in typer
  * the panel where "help" and other built in options are put

### Add remaining CLI interfaces

* Interface for `core.manage_models`
* Interface for `core.manage_audio`
* Interfaces for individual pipeline functions defined in `core.generate_song_covers`

## python package management

* need to make project version (in `pyproject.toml`) dynamic so that it is updated automatically when a new release is made
* once diffq-fixed is used by audio-separator we can remove the url dependency on windows
  * we will still need to wait for uv to make it easy to install package with torch dependency
  * also it is still necessary to install pytorch first as it is not on pypi index
* figure out way of making ./urvc commands execute faster
  * when ultimate rvc is downloaded as a pypi package the exposed commands are much faster so investigate this
* update dependencies in pyproject.toml
  * use latest compatible version of all packages
  * remove commented out code, unless strictly necessary

## Audio separation

* expand back-end function(s) so that they are parametrized by both model type as well as model settings
  * Need to decide whether we only want to support common model settings or also settings that are unique to each model
    * It will probably be the latter, which will then require some extra checks.
  * Need to decide which models supported by `audio_separator` that we want to support
    * Not all of them seem to work
    * Probably MDX models and MDXC models
    * Maybe also VR and demucs?
  * Revisit online guide for optimal models and settings
* In multi-step generation tab
  * Expand audio-separation accordion so that model can be selected and appropriate settings for that model can then be selected.
    * Model specific settings should expand based on selected model
* In one-click generation
  * Should have an "vocal extration" option accordion
    * Should be able to choose which audio separation steps to include in pipeline
      * possible steps
        * step 1: separating audio form instrumentals
        * step 2: separating main vocals from background vocals:
        * step 3: de-reverbing vocals
      * Should pick steps from dropdown?
      * For each selected step a new sub-accordion with options for that step will then appear
        * Each accordion should include general settings
        * We should decide whether model specific settings should also be supported
        * We Should also decide whether sub-accordion should setting for choosing a model and if so render specific settings based the chosen model
    * Alternative layout:
      * have option to choose number of separation steps
      * then dynamically render sub accordions for each of the selected number of steps
        * In this case it should be possible to choose models for each accordion
          * this field should be iniitally empty
        * Other setttings should probably have sensible defaults that are the same
      * It might also be a good idea to then have an "examples" pane with recommended combinations of extractions steps
      * When one of these is selected, then the selected number of accordions with the preset settings should be filled out
  * optimize pre-processing
    * check <https://github.com/ArkanDash/Multi-Model-RVC-Inference>
  * Alternatives to `audio-separator` package:
    * [Deezer Spleeter](https://github.com/deezer/spleeter)
      * supports both CLI and python package
    * [Asteroid](https://github.com/asteroid-team/asteroid)
    * [Nuzzle](https://github.com/nussl/nussl)

## GitHub

### Actions

* linting with Ruff
* typechecking with Pyright
* running all tests
* automatic building and publishing of project to pypi
  * includes automatic update of project version number
* or use pre-commit?

### README

* Fill out TBA sections in README
* Add note about not using with VPN?
* Add different emblems/badges in header
  * like test coverage, build status, etc. (look at other projects for inspiration)
* spice up text with emojis (look at tiango's projects for inspiration)

### Releases

* Make regular releases like done for Applio
  * Will be an `.exe` file that when run unzips contents into application folder, where `./urvc run` can then be executed.
  * Could it be possible to have `.exe` file just start webapp when clicked?
* Could also include pypi package as a release?

* use pyinstaller to install app into executable that also includes sox and ffmpeg as dependencies (DLLs)

### Other

* In the future consider detaching repo from where it is forked from:
  * because it is not possible to make the repo private otherwise
  * see: <https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/working-with-forks/detaching-a-fork>

## Incorporate upstream changes

* Incorporate RVC code from [rvc-cli](https://github.com/blaisewf/rvc-cli) (i.e. changes from Applio)
  * more options for voice conversion and more efficient voice conversion
  * batch conversion sub-tab
  * TTS tab
  * Model training tab
  * support more pre-trained models
    * sub-tab under "manage models" tab
  * support for querying online database with many models that can be downloaded
  * support for audio and model analysis.
  * Voice blending tab
* Incorporate latest changes from [RVC-WebUI](https://github.com/RVC-Project/Retrieval-based-Voice-Conversion-WebUI)

## Vocal Conversion

* clone /fork applio huggingface repo and then download from your fork in prerequities_donwload.py

* move all post processing to specific postprocessing step
  * not part of voice conversion step

* incorporate autotune as a post-processing step with separate package instead of as part of vocal conversion

* parallelize different steps in the pipeline
  * two pitch shifts operations that are currently executed sequentially should be executed in parallel because they are done on cpu.
  * application of different f0 extraction methods should also be done in parallel.

* Add more pitch detection methods
  * pm
  * harvest
  * dio
  * rvmpe+

  * add harvest, pm, dio f0 methods back in?

* support arbitrary combination of pitch detection algorithms
  * use different method than median for combining extracted f0 values?

* formant shifting currently does not make a difference because
  * under the hood `tftPitchShift.shiftpitch` is called to pitch shift input audio with `quefrency` multiplied by `1e-3` which makes it almost equal to `0`. that might be too a value to have any effect
* potentially use another library for formant shifting. for example praatio or parselmouth
  * one solution: <https://github.com/drfeinberg/Parselmouth-Guides/blob/master/ManipulatingVoices.ipynb> (look at buttom)
  * also, formant shifting is primarily meant for male to female and vice versa conversions without changing the pitch of the voice so it would actually be very useful as we can dispense wit hpitch shifting in that case
  * can also use praatio for this: <https://timmahrt.github.io/praatIO/praatio/praat_scripts.html>

* f0-curve file do not really work so the --f0-file parameter does not currently make sense for the inference step
  * should probably remove it from the inference step
  * we can add it back in once if we are able to fix the algorithm that
  * uses custom f0 curve files but that is probably way down the line

* audio upscaler is extremely slow
  * mention this in applio and rvc-cli
  * also try to use audio upscaling in the app and verify it takes long there
  * try and find a better alternatively to the current audio upscaler package
    * or perhaps optimize it yourself.
  * also audio upscaling does not really make sense for inference as the audio is downsampled to 16kHz
    * only makes sense if the audio is below 16kHz in sample rate which is unlikely
    * so maybe we should just remove the audio upscaler from the pipeline
  * conclusion: remove audio upscaler from inference pipeline
* audio upscaler model should be downloaded at initialization and not laziely (when first used)
* fix that audio upscaler downsload pyorch_model.bin to cwd

* currently we are not downloading any-pretraineds. Potentially enabling downloading of all when it is needed later (perhaps when we add training tab?)

* info on custom embedder models
  * when using a custom embedder model you have to use a fine-tuned model trained using that embedder model during inference.
    * its hard to find such models only so better fine tune your own model in that case
  * the custom embedder model should be a folder with a pytorch_model.bin file and a config.json file

* Implement multi-gpu Inference

## TTS conversion

* also include original edge voice as output
  * source: <https://github.com/litagin02/rvc-tts-webui>

## Model management

### Training models

* have learning rate for training
  * source: <https://github.com/gitmylo/audio-webui>
* have a quick training button
  * or have preprocess dataset, extract features and generate index happen by default
* Support a loss/training graph
  * source: <https://github.com/gitmylo/audio-webui>

### Download models

* Support batch downloading multiple models
  * requires a tabular request form where both a link column and a name column has to be filled out
  * we can allow selecting multiple items from public models table and then copying them over
* support quering online database for models matching a given search string like what is done in applio app
  * first n rows of online database should be shown by default in public models table
    * more rows should be retrieved by scrolling down or clicking a button
  * user search string should filter/narrow returned number of rows in public models table
  * When clicking a set of rows they should then be copied over for downloading in the "download" table
* support a column with preview sample in public models table
  * Only possible if voice snippets are also returned when querying the online database
* Otherwise we can always support voice snippets for voice models that have already been downloaded
  * run model on sample text ("quick brown fox runs over the lazy") after it is downloaded
  * save the results in a `audio/model_preview` folder
  * Preview can then be loaded into a preview audio component when selecting a model from a dropdown
  * or if we replace the dropdown with a table with two columns we can have the audio track displayed in the second column

### Model analysis

* we could provide a new tab to analyze an existing model like what is done in applio
  * or this tab could be consolidated with the delete model tab?

* we could also provide extra model information after model is downloaded
  * potentialy in dropdown to expand?

## Audio management

### General

* Support audio information tool like in applio?
  * A new tab where you can upload a song to analyze?
* more elaborate solution:
  * tab where where you
    * can select any song directory
    * select any step in the audio generation pipeline
    * then select any intermediate audio file generated in that step
    * Then have the possibility to
      * Listen to the song
      * see a table with its metadata (based on its associated `.json` file)
        * add timestamp to json files so they can be sorted in table according to creation date
      * And other statistics in a separate component (graph etc.)
  * Could have delete buttons both at the level of song_directory, step, and for each song?
  * Also consider splitting intermediate audio tracks for each step in to subfolder (0,1,2,3...)

## Other settings

* rework other settings tab
  * this should also contain other settings such as the ability to change the theme of the app
  * there should be a button to apply settings which will reload the app with the new settings

## Audio post-processing

* Support more effects from the `pedalboard` pakcage.
  * Guitar-style effects: Chorus, Distortion, Phaser, Clipping
  * Loudness and dynamic range effects: Compressor, Gain, Limiter
  * Equalizers and filters: HighpassFilter, LadderFilter, LowpassFilter
  * Spatial effects: Convolution, Delay, Reverb
  * Pitch effects: PitchShift
  * Lossy compression: GSMFullRateCompressor, MP3Compressor
  * Quality reduction: Resample, Bitcrush
  * NoiseGate
  * PeakFilter

## Audio Mixing

* Add main gain loudness slider?
* Add option to equalize output audio with respect to input audio
  * i.e. song cover gain (and possibly also more general dynamics) should be the same as those for source song.
  * check to see if pydub has functionality for this
  * otherwise a simple solution would be computing the RMS of the difference between the loudness of the input and output track

  ```python
    rms = np.sqrt(np.mean(np.square(signal)))
    dB  = 20*np.log10(rms)
    #add db to output file in mixing function (using pydub)
  ```

  * When this option is selected the option to set main gain of ouput should be disabled?

* add more equalization options
  * using `pydub.effects` and `pydub.scipy_effects`?

## Custom UI

* Experiment with new themes including [Building new ones](https://www.gradio.app/guides/theming-guid)
  * first of all make new theme that is like the default gradio 4 theme in terms of using semi transparent orange as the main color and semi-transparent grey for secondary color. The new gradio 5 theme is good apart from using solid colors so maybe use that as base theme.
  * Support both dark and light theme in app?
  * Add Support for changing theme in app?
  * Use Applio theme as inspiration for default theme?
* Experiment with using custom CSS
  * Pass `css = {css_string}` to `gr.Blocks` and use `elem_classes` and `elem_id` to have components target the styles define in the CSS string.
* Experiment with [custom DataFrame styling](https://www.gradio.app/guides/styling-the-gradio-dataframe)
* Experiment with custom Javascript
* Look for opportunities for defining new useful custom components

## Real-time vocal conversion

* Should support being used as OBS plugin
* Latency is real issue
* Implementations details:
  * implement back-end in Rust?
  * implement front-end using svelte?
  * implement desktop application using C++ or C#?
* see <https://github.com/w-okada/voice-changer> and <https://github.com/RVC-Project/obs-rvc> for inspiration

## AI assistant mode

* similar to vocal conversion streaming but instead of converting your voice on the fly, it should:
  * take your voice,
  * do some language modelling (with an LLM or something)
  * then produce an appropriate verbal response
* We already have Kyutais [moshi](https://moshi.chat/?queue_id=talktomoshi)
  * Maybe that model can be finetuned to reply with a voice
  * i.e. your favorite singer, actor, best friend, family member.

## Ultimate RVC bot for discord

* maybe also make a forum on  discord?

## Make app production ready

* have a "report a bug" tab like in applio?
* should have separate accounts for users when hosting online
  * use `gr.LoginButton` and `gr.LogoutButton`?

* deploy using docker
  * See <https://www.gradio.app/guides/deploying-gradio-with-docker>
* Host on own web-server with Nginx
  * see <https://www.gradio.app/guides/running-gradio-on-your-web-server-with-nginx>

* Consider having concurrency limit be dynamic, i.e. instead of always being 1 for jobs using gpu consider having it depend upon what resources are available.
  * We can app set the GPU_CONCURRENCY limit to be os.envrion["GPU_CONCURRENCY_LIMIT] or 1 and then pass GPU_CONCURRENCY as input to places where event listeners are defined

## Colab notebook

* find way of saving virtual environment with python 3.11 in colab notebook (DIFFICULT TO IMPLEMENT)
  * so that this environment can be loaded directly rather than downloading all dependencies every time app is opened

## Testing

* Add example audio files to use for testing
  * Should be located in `audio/examples`
  * could have sub-folders `input` and `output`
    * in `output` folder we have `output_audio.ext` files each with a corresponding `input_audio.json` file containing metadata explaining arguments used to generate output
    * We can then test that actual output is close enough to expected output using audio similarity metric.
* Setup unit testing framework using pytest
