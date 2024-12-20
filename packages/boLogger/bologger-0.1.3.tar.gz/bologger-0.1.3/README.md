# What is this package?

This package is an advanced logging system that allows the user to create custom and preset logs, with colour.

# Installation

```bash
pip install boLogger --upgrade
```

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
) # This is used to create deafults for the custom_log() method and 

.custom_log(
    text: str,  
    title: str, 
    color: str, 
    bold: bool, 
    underlined: bool
) # If you already have a deafult set you will only need to enter the text param
  # But if you have not, you will need to enter all params
        

.view_deafult() # method to view the current deafult settings

.add_color(colour) # your own colour code (must start with '\033[')
```

# Example Usage

```py
# Make sure to define the class
mylogger = Logging()
print(mylogger) # Explains the module
mylogger.header("Header")
mylogger.info("Info")
mylogger.warning("Warning")
mylogger.error("Error")
mylogger.success("Success")
mylogger.beans("Beans")
mylogger.info("This is a very long log message that is going to spill over to the next line and needs to be properly indented for better readability.")


customLogger = CustomLog()
print(customLogger) # Explains the module
customLogger.set_default(title="beansareyummy", color='Blue') # Bold and underlined are automatically set to false
customLogger.view_deafult()
customLogger.custom_log("custom")
customLogger.info("custom")
```

# Features

- Colour
- Create your own custom logger
- Text wrapping (the text will never be on the same level as the logger info)
- Easy use


