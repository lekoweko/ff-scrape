# ff-scrape
scrape ff.net

## How to use 

1. Fork and clone the repo (or copy and paste it into an IDE if that's your thing). 
2. Import/install the necessary packages. You may need to install the driver manually. 
3. In `scrape_story()` input a string of the story URL you'd like to scrape. 
- Example 1: `scrape_story('https://www.fanfiction.net/s/<story-id>')`
- Example 2: `scrape_story('https://www.fanfiction.net/s/<story-id>/1/<story-title>')`
4. Run the program. The program will output as a text file. 


## Example output 
```
{
  'Fandom': 'The Great Story', 
  'Title': "The Greater Story: Part II", 
  'Author': 'april2324', 
  'Author ID': 1000000, 
  'Publisher': 'https://fanfiction.net', 
  'Story URL': 'https://www.fanfiction.net/s/000000/1/the-greater-story-part-two', 
  'Author URL': 'https://fanfiction.net/u/000000/april2324', 
  'Story Data': 
    [
      'Rated: Fiction T ', 
      ' English ', 
      ' Drama/Friendship ', 
      ' T. West, A. Jones. ', 
      ' Chapters: 3 ', 
      ' Words: 8,000 ', 
      ' Reviews: 113 ', 
      ' Favs: 216 ', 
      ' Follows: 345 ', 
      ' Updated: Dec 16, 2007 ', 
      ' Published: Dec 8, 2007 ', 
      ' Status: Complete ', 
      ' id: 000000 '
     ], 
  'Summary': "What if Terry made a wish to save April at the end of The Great Story?", 
  'Story': 'My story in human readable text.', 
  'Raw Story': '<p>My story in html-preserved text.</p>'
}
```

## Acknowledgements 

[Smilli's fanfiction scraping project](https://github.com/smilli/fanfiction) provided some inspiration for this project. 
