import sublime, sublime_plugin
import re

#
# Pseudoclass completion
#
element_pseudoclasses       = [":first", ":last"]
header_pseudoclasses        = [":first-page", ":left-page", ":right-page"]
enumeration_pseudoclasses   = [":enumerator"]
footnote_pseudoclasses      = [":anchor"]

pseudoclasses_by_selector = {
    "list-all":         element_pseudoclasses + enumeration_pseudoclasses,
    "list-ordered":     element_pseudoclasses + enumeration_pseudoclasses,
    "list-unordered":   element_pseudoclasses + enumeration_pseudoclasses,

    "inline-footnote":      element_pseudoclasses + footnote_pseudoclasses,
    "inline-annotation":    element_pseudoclasses + footnote_pseudoclasses,

    "area-header":      header_pseudoclasses,
    "area-footer":      header_pseudoclasses,

    "defaults":         []
}

#
# Property / Value completion
#
length_options  = ["${1:<length>}em", "${1:<length>}ex", "${1:<length>}en", "${1:<length>}pt", "${1:<length>}%", "${1:<length>}cm", "${1:<length>}mm", "${1:<length>}in"]

color_snippet   = ("#${0:000000}", ["rgb(${1:red}, ${2:green}, ${3:blue})", "#${0:000000}"])
number_snippet  = "${1:number}"
length_snippet  = ("${1:length}", length_options)
bool_snippet    = ("${1:yes}", ["yes", "no"])

element_completions = {
    "style-title":          "\"${1:Title for RTF Style}\"",

    "font-family":          "\"${1:Helvetica}\"",
    "font-style":           "\"${1:UltraLight}\"",
    "font-size":            length_snippet,
    "font-weight":          ["bold", "normal"],
    "font-slant":           ["italic", "normal"],
    "baseline-shift":       ["normal", "superscript", "subscript"],
    "character-spacing":    length_snippet,

    "font-color":           color_snippet,
    "background-color":     color_snippet,

    "underline":            ["single", "none"],
    "underline-color":      color_snippet,

    "strikethrough":        ["signle", "none"],
    "strikethrough-color":  color_snippet,

    "visibility":           ["visible", "hidden"],
    
}

media_completions = {
    "margin-left":          length_snippet,
    "margin-right":         length_snippet
}

footnote_completions = {
    "footnote_visibility":  ["visible", "hidden"], 
}

paragraph_completions = {
    "text-alignment":       ["left", "center", "right", "justify"],
    "margin-top":           length_snippet,
    "margin-left":          length_snippet,
    "margin-right":         length_snippet,
    "marign-bottom":        length_snippet,
    "line-height":          ("$1", ["${1:auto}"] + length_options),
    "first-line-indent":    length_snippet,
    "page-break":           ["none", "after", "before"],
    "keep-with-following":  bool_snippet,
    "default-tab-interval": length_snippet,
    "tab-positions":        "[${1:10em}, ${2:20em}, ${3:30em}]",
    "tab-alignments":       "[${1:left}, ${2:center}, ${3:right}]",
    "hyphenation":          bool_snippet
}

divider_completions = {
    "content":              "\"${1:Content of divider}\""
}

itemized_group_completions = {
    "itemization":          ["itemize", "none"],
    "item-spacing":         length_snippet,
    "text-inset":           length_snippet,
    "enumeration_format":   "\"${1:%p}\"",
    "enumeration-style":    ["decimal", "lowercase-roman", "uppercase-roman", "lowercase-alpha", "uppercase-alpha"]
}

header_completions = {
    "content":              ["none", "page-number", "heading"],
    "top-spacing":          length_snippet,
    "bottom-spacing":       length_snippet
}

footnote_area_completions = {
    "top-spacing":          length_snippet,
    "divider-position":     length_snippet,
    "divider-width":        length_snippet,
    "divider-length":       length_snippet,
    "divider-spacing":      length_snippet,    
    "anchor-alignment":     ["left", "right"],
    "anchor-inset":         length_snippet,
    "text-inset":           ["left", "right"]
}

document_settings_completions = {
    "column-count":         number_snippet,
    "column-spacing-width": length_snippet,
    "page-number-reset":    ["none", "per-section"],
    "page-number-format":   "\"$1{- %p -}\"",
    "page-number-style":    ["decimal", "lowercase-alpha", "uppercase-alpha", "lowercase-roman", "uppercase-roman"],

    "page-orientation":     ["landscape", "portrait"],
    "page-height":          length_snippet,
    "page-width":           length_snippet,
    "page-inset-top":       length_snippet,
    "page-inset-inner":     length_snippet,
    "page-inset-outer":     length_snippet,
    "page-inset-bottom":    length_snippet,
    "page-binding":         ["left", "right"],
    "two-sided":            bool_snippet,
    "section-break":        ["heading-1", "heading-2", "heading-3", "heading-4", "heading-5", "heading-6", "paragraph-divider", "none"],
    "footnote-style":       ["decimal", "lowercase-alpha", "uppercase-alpha", "lowercase-roman", "uppercase-roman", "chicago-style-manual"],
    "footnote-placement":   ["end-of-page", "end-of-section", "end-of-document"],
    "footnote-enumeration": ["per-page", "per-section", "continuous"],

    "locale":               "\"${1:en}\""
}

paragraph_profile_completions = dict(element_completions.items() + paragraph_completions.items())
list_profile_completions = dict(element_completions.items() + paragraph_completions.items() + itemized_group_completions.items())

completions_by_selector = {
    "document-settings":    document_settings_completions,
    "area-header":          dict(paragraph_profile_completions.items() + header_completions.items()),
    "area-footer":          dict(paragraph_profile_completions.items() + header_completions.items()),
    "area-footnotes":       dict(paragraph_profile_completions.items() + footnote_area_completions.items()),

    "defaults":             paragraph_profile_completions,
    
    "paragraph":            paragraph_profile_completions,
    "paragraph-divider":    dict(paragraph_profile_completions.items() + divider_completions.items()),
    "paragraph-figure":     paragraph_profile_completions,

    "heading-all":          paragraph_profile_completions,
    "heading-1":            paragraph_profile_completions,
    "heading-2":            paragraph_profile_completions,
    "heading-3":            paragraph_profile_completions,
    "heading-4":            paragraph_profile_completions,
    "heading-5":            paragraph_profile_completions,
    "heading-6":            paragraph_profile_completions,

    "block-all":            paragraph_profile_completions,
    "block-code":           paragraph_profile_completions,
    "block-comment":        paragraph_profile_completions,
    "block-quote":          paragraph_profile_completions,
    "block-raw":            paragraph_profile_completions,

    "list-all":             list_profile_completions,
    "list-ordered":         list_profile_completions,
    "list-unordered":       list_profile_completions,

    "inline-code":          element_completions,
    "inline-comment":       element_completions,
    "inline-delete":        element_completions,
    "inline-emphasis":      element_completions,
    "inline-link":          element_completions,
    "inline-mark":          element_completions,
    "inline-raw":           element_completions,
    "inline-strong":        element_completions,

    "inline-footnote":      dict(element_completions.items() + footnote_completions.items()),
    "inline-annotation":    dict(element_completions.items() + footnote_completions.items()),

    "media-image":          dict(element_completions.items() + media_completions.items()),

    "ulysses-escape-character":     element_completions,
    "ulysses-escape":               element_completions,
    "ulysses-tag":                  element_completions,
    "ulysses-whitespace":           element_completions
}

# All completions that may apply to content
fallback_completions = dict(element_completions.items() + media_completions.items() + paragraph_completions.items() + divider_completions.items() + itemized_group_completions.items())

#
# Selector completion
#
all_selectors = sorted(completions_by_selector.keys() + ["@${0:Mixin}"])


#
# Parser
#
pseudoclass_regex = re.compile('(?<!\@)([a-zA-Z0-9\-]+)(?:[\:\@][a-zA-Z0-9\-]+)*\s*:$')
style_identifier_regex = re.compile('(?<!\@)([a-zA-Z0-9\-]+)\s*$')
style_block_regex = re.compile('([a-zA-Z0-9\-]+)(\s*\:\s*[a-zA-Z0-9\s\:\@\,]+)?\s*\{[^\{]*$')
property_value_regex = re.compile('([a-zA-Z0-9\-]+)\:\s*$')
placeholder_regex = re.compile('\$\{[0-9]\:([^\}]+)\}')

class UlyssesStyleSheetCompletions(sublime_plugin.EventListener):
    def on_query_completions(self, view, prefix, locations):
        
        # Ignore non-ULSS-Files
        if not view.match_selector(locations[0], "source.ulss"):
            return     

        # Ignore comments
        if view.match_selector(locations[0], "comment.ulss"):
            return

        # Pseudoclasses
        if view.match_selector(locations[0], "meta.selector.ulss") or view.match_selector(locations[0] -1, "meta.selector.ulss"):
            return self.autocomplete_pseudoclasses(view, prefix, locations)

        # Definitions: keys and values
        elif view.match_selector(locations[0], "meta.style-definition.ulss") or view.match_selector(locations[0] -1, "meta.style-definition.ulss"):
            return self.autocomplete_definitions(view, prefix, locations)

        # Selectors
        else:
            return self.autocomplete_selectors(view, prefix, locations)

    def autocomplete_pseudoclasses(self, view, prefix, locations):
        suggestions = list()

        location = locations[0] - len(prefix)
        line_prefix = view.substr(sublime.Region(view.line(location).begin(), location))
        current_selector_match = re.search(pseudoclass_regex, line_prefix)           

        # Do not provide pseudoclasses for mixins
        if "@" in line_prefix:
            return ([], sublime.INHIBIT_WORD_COMPLETIONS)

        # Autocomplete selectors if not a prefix
        if (current_selector_match == None):
           return self.autocomplete_selectors(view, prefix, locations)

        # Autocomplete pseudoclass matching to selector
        if (current_selector_match.group(1) in pseudoclasses_by_selector):
            completions = pseudoclasses_by_selector[current_selector_match.group(1)]
        else:
            completions = element_pseudoclasses

        for pseudoclass in completions:
            suggestions.append((pseudoclass, pseudoclass))

        return (suggestions, sublime.INHIBIT_WORD_COMPLETIONS)

    def autocomplete_selectors(self, view, prefix, locations):
        suggestions = list()

        # Add relation operators if possible
        location = locations[0] - len(prefix)
        line_prefix = view.substr(sublime.Region(view.line(location).begin(), location))
        line_suffix = view.substr(view.line(sublime.Region(location, view.line(location).end())))
        current_selector_match = re.search(style_identifier_regex, line_prefix)           

        # Mixin-only selector
        if "@" in line_prefix:
            if not ":" in line_prefix:
                return ([(": @Mixin", ": @${0:Mixin}")], sublime.INHIBIT_WORD_COMPLETIONS)
            else:
                return ([(", @Mixin", ", @${0:Mixin}")], sublime.INHIBIT_WORD_COMPLETIONS)

        # Other selectors
        should_append_block = not "{" in line_suffix

        for key in all_selectors:
            if should_append_block:
                suggestions.append((re.sub(placeholder_regex, '\g<1>', key), key + " {\n\t$1\n}\n"))
            else:
                suggestions.append((re.sub(placeholder_regex, '\g<1>', key), key + " "))

        if (current_selector_match != None):
            suggestions = [("+\tSuccessor", "+"), (">\tChild", ">"), (":pseudoclass", ":$0"), (": @Mixin", ": @${0:Mixin}")] + suggestions

        return (suggestions, sublime.INHIBIT_WORD_COMPLETIONS)        

    def autocomplete_definitions(self, view, prefix, locations):
        location = locations[0] - len(prefix)
        line = view.substr(sublime.Region(view.line(location).begin(), location))
        current_keyword_match = re.search(property_value_regex, line)

        #
        # Get style profile
        #
        block = view.substr(sublime.Region(0, location))
        stylename_match = re.search(style_block_regex, block)
        completions = None

        if (stylename_match != None) and (stylename_match.group(1) in completions_by_selector):
            completions = completions_by_selector[stylename_match.group(1)]
        else:
            completions = fallback_completions

        #
        # Get autocompletion triggers
        if current_keyword_match:
            suggestions = self.autocomplete_style_values(current_keyword_match.group(1), completions)
        else:
            suggestions = self.autocomplete_style_keys(completions)
    
        return (suggestions, sublime.INHIBIT_WORD_COMPLETIONS)        

    def autocomplete_style_values(self, current_keyword, completions):
        suggestions = list()
        suggestion_descriptor = completions[current_keyword]

        if (isinstance(suggestion_descriptor, tuple)):
            suggestion_descriptor = suggestion_descriptor[1]
        
        if (isinstance(suggestion_descriptor, str)):
            suggestions.append((re.sub(placeholder_regex, '\g<1>', suggestion), suggestion))
        else:
            for suggestion in sorted(suggestion_descriptor):
                suggestions.append((re.sub(placeholder_regex, '\g<1>', suggestion), suggestion))

        return suggestions

    def autocomplete_style_keys(self, completions):
        suggestions = list()

        for key, value in sorted(completions.iteritems()):
            suggested_key = (key + ":") + "".ljust(((24 - (len(key) + 1)) / 4) + 1, '\t')

            if (isinstance(value, str)):
                suggestions.append((key, suggested_key + value))
            elif (isinstance(value, tuple)):
                suggestions.append((key, suggested_key + value[0]))    
            elif (isinstance(value, list)):
                suggestions.append((key, suggested_key + "$0"))    

        return suggestions
