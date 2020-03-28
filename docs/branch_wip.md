# Validating this approach
* Is it ok to keep adding columns like this?
    * Consider clearer labelling / replace labels in codeshare column with simpler. 
    * e.g. AltID, MainID, OnlyID

# finding Duplicates
* filter by actual time
    * If actual time & scheduled time & origin/destination are the same, flag this.
* add origin and destination airport to help find if there's any true duplicates.

# Changes for Other Branches
* Change accept to Y/y like "rm -i" does
