(*
script to export all safari tabs to stdout
in a simple tab-delimited format

based on:

"Export All Safari Tabs in All Open Windows to a Markdown File"

// SCRIPT PAGE
	http://hegde.me/urlsafari
   
// ORIGINAL SCRIPT ON WHICH THIS SCRIPT IS BUILT
	http://veritrope.com/code/export-all-safari-tabs-to-a-text-file

// TERMS OF USE:
	This work is licensed under the Creative Commons Attribution-NonCommercial-ShareAlike 3.0 Unported License. 

	To view a copy of this license, visit http://creativecommons.org/licenses/by-nc-sa/3.0/ or send a letter to Creative Commons, 444 Castro Street, Suite 900, Mountain View, California, 94041, USA.
*)
----------------------------------------------------------------------------------------

set tabChar to character id 9
set buffer to ""

-- GET TABS FROM SAFARI
set window_count to 1
tell application "Safari"
	-- doesn't seem necessary to activate the app
	--activate
	set safariWindow to windows
	repeat with w in safariWindow
		try
			if (tabs of w) is not {} then
				
				repeat with t in (tabs of w)
					set TabTitle to ("[" & name of t & "]")
					set TabURL to ("(" & URL of t & ")")
					set tmpline to window_count & tabChar & TabTitle & tabChar & TabURL & linefeed
					--log (tmpline)
					set buffer to buffer & tmpline
				end repeat
			end if
		end try
		set window_count to window_count + 1
	end repeat
end tell

-- some witchery to convert the buffer to text
set old_delim to AppleScript's text item delimiters
set AppleScript's text item delimiters to return
set text_out to buffer as text
set AppleScript's text item delimiters to old_delim

return text_out
