# What is this package?

This package is an advanced logging system that allows the user to create custom and preset logs, with colour.

# Example Usage

```py
# Make sure to define the class
    mylogger = Logging()
    print(mylogger)
    mylogger.header("Header")
    mylogger.info("Info")
    mylogger.warning("Warning")
    mylogger.error("Error")
    mylogger.success("Success")
    mylogger.beans("Beans")
    mylogger.info("This is a very long log message that is going to spill over to the next line and needs to be properly indented for better readability.")

    
    customLogger = CustomLog()
    print(customLogger)
    customLogger.set_default(title="beansareyummy", color='Blue')
    customLogger.view_deafult()
    customLogger.custom_log("custom")
    customLogger.info("custom")
```

# Features

- Colour
- Create your own custom logger
- Text wrapping (the text will never be on the same level as the logger info)
- Easy use


