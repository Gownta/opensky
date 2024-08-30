tell application "Google Chrome"
    activate
    set activeTab to active tab of first window
    set URL of activeTab to "https://planefinder.net/data/airline/ACA/flights"
end tell

delay 1

tell application "System Events"
    keystroke "u" using {command down, option down}
end tell

delay 0.5

tell application "System Events"
    keystroke "a" using {command down}
    delay 0.1
    keystroke "c" using {command down}
end tell

tell application "TextMate"
    activate
    keystroke "v" using {command down}
end tell

