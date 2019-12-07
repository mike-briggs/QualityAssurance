# 🐨 KoalityAssured 🐨

## Prerequisites

python 3.8 (or higher)

## Development

Devlopment was all done using:

  Windows 10
  Visual Studio Code/Atom
  

## Usage

To run the weekly transaction script you must be in the folder:

```
/src/transaction_sessions
```

simply running the command:
```
python weekly.py
```

will then execute the daily.py script x 5 running the backend at the end of each loop.

Daily.py:
- calls frontend.py
- input arguments: valid_accounts, chosen_output_filepath_name

Because of the file structure, files do not require many system arguments to be passed, it can assume that (for example) the "day_merged_out.txt" file inside of that days folder is simply the merged transaction summary for that day.

Using the frontend on its own can be done by executing:

```
python frontend.py [valid_accounts_path] [chosen_output_filename]
```

## Contributing

Connor Crowe            (20009994)

Jordan Mack             (20005220)

Michael Briggs          (20013906)

Sasanka Wickramasinghe  (10192504)

## License
[MIT](https://choosealicense.com/licenses/mit/)
