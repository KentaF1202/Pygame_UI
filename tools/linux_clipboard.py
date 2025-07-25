import sys
import subprocess

def copy_to_clipboard(text):
    # If platform isnt linux, dont run
    if (sys.platform != "linux"):
        return
    
    # Copies text to clipboard
    try:
        # Popen creates a new process.
        # stdin=subprocess.PIPE allows us to write to xclip's standard input.
        # '-selection', 'clipboard' ensures it uses the standard clipboard (Ctrl+C/V).
        process = subprocess.Popen(['xclip', '-selection', 'clipboard'], stdin=subprocess.PIPE)
        # Write the text to xclip's stdin. encode() is important as pipes handle bytes.
        process.communicate(input=text.encode('utf-8'))
        print(f"Text '{text}' copied to clipboard via xclip.")
    except FileNotFoundError:
        print("Error: 'xclip' command not found. Please ensure it is installed and in your PATH.")
    except Exception as e:
        print(f"An error occurred while copying to clipboard: {e}")

    return

def paste_from_clipboard():
    # If platform isnt linux, dont run
    if (sys.platform != "linux"):
        return
    
    # Returns text as string from clipboard
    try:
        # Popen creates a new process.
        # stdout=subprocess.PIPE allows us to read from xclip's standard output.
        # '-selection', 'clipboard' ensures it reads from the standard clipboard.
        # '-o' (output) tells xclip to print the clipboard content.
        process = subprocess.Popen(['xclip', '-selection', 'clipboard', '-o'], stdout=subprocess.PIPE)
        # Read the output and decode it from bytes to a string.
        output, _ = process.communicate()
        pasted_text = output.decode('utf-8').strip()
        print(f"Text '{pasted_text}' pasted from clipboard via xclip.")
        return pasted_text
    except FileNotFoundError:
        print("Error: 'xclip' command not found. Please ensure it is installed and in your PATH.")
        return ""
    except Exception as e:
        print(f"An error occurred while pasting from clipboard: {e}")
        return ""