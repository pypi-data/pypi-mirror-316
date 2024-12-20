# What is this package?

This package is an advanced logging system that allows the user to create custom and preset logs, with colour.

# Installation

```bash
pip install boLogger --upgrade
```

# Features

- Colour
- Create your own custom logger
- Text wrapping (the text will never be on the same level as the logger info)
- Easy use

# Options

### Colours

Black, Red, Green, Yellow, Blue, Purple, Cyan, White, BBlack, BRed, BGreen, BYellow, BBlue, BPurple, BCyan, BWhite
(B stands for bright)

### Options for Logging()

```py
.header(text)
.info(text)
.warning(text)
.error(text)
.success(text)
```

### Options for CustomLog()

CustomLog() includes everything in the Logging() class and more
```py
.set_deafult(
    title: str, 
    color: str, 
    bold: bool, 
    underlined: bool
) # This is used to create deafults for the custom_log() method
  # Meaning if the user wants to use the cutom_log() method 
  # They only need to use the text parameter 

.custom_log(
    text: str,  
    title: str, 
    color: str, 
    bold: bool, 
    underlined: bool
) # If you already have a deafult set you will only need to enter the text param
  # But if you have not, you will need to enter all params
        
# Method to view the current deafult settings
# It returns it, not printing
.view_deafult() 

.add_color(colour) # your own colour code (must start with '\033[')
```

# Example Usage

```py
### Logging()
print(Logging()) # Explains the module

.header("Header")

.info("Info")

.warning("Warning")

.error("Error")

.success("Success")

.beans("Beans")

.info("This is a very long log message that is going to spill over to the next line and needs to be properly indented for better readability.")



### CustomLog()
# Explains the module
print(CustomLog()) 

# Bold and underlined are automatically set to false
.set_default(title="beansareyummy", color='Blue') 

.view_deafult()

.custom_log("custom")

.info("custom")
```



