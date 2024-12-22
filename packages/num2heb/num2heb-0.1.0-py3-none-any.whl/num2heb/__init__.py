def number_to_words(num):
    if not isinstance(num, int):
        raise ValueError("The input must be an integer.")

    # Define the number components
    units = ["", "אחד", "שניים", "שלושה", "ארבעה", "חמישה", "שישה", "שבעה", "שמונה", "תשעה"]
    # feminine_units = ["", "אחת", "שתיים", "שלוש", "ארבע", "חמש", "שש", "שבע", "שמונה", "תשע"]
    teens = ["עשרה", "אחד עשר", "שניים עשר", "שלושה עשר", "ארבעה עשר", "חמישה עשר", "שישה עשר", "שבעה עשר", "שמונה עשר", "תשעה עשר"]
    tens = ["", "", "עשרים", "שלושים", "ארבעים", "חמישים", "שישים", "שבעים", "שמונים", "תשעים"]
    hundreds = ["", "מאה", "מאתיים", "שלוש מאות", "ארבע מאות", "חמש מאות", "שש מאות", "שבע מאות", "שמונה מאות", "תשע מאות"]
    big_numbers = ["", "אלף", "מיליון", "מיליארד", "טריליון", "קוואדריליון", "קוונטיליון", "סקסטיליון", "ספטיליון", "אוקטיליון", "נוניליון"]

    # Handle zero
    if num == 0:
        return "אפס"

    # Break the number into chunks of 3 digits each
    def chunk_number(n):
        parts = []
        while n > 0:
            parts.append(n % 1000)
            n //= 1000
        return parts[::-1]

    def chunk_to_words(chunk):
        words = []
        addVav = False
        if chunk >= 100:
            words.append(hundreds[chunk // 100])
            chunk %= 100
            addVav = True
        if 10 <= chunk < 20:
            t = teens[chunk - 10]
            if addVav:
                t = "ו" + t
                addVav = False
            words.append(t)
        else:
            if chunk >= 20:
                t=tens[chunk // 10]
                if addVav and chunk % 10 == 0:
                    t = "ו" + t
                    addVav = False
                else:
                    addVav = True
                words.append(t)
                chunk %= 10
            if chunk > 0:
                if addVav:  # If there are already words (i.e., tens are present)
                    words.append("ו" + units[chunk])  # Add "ו" before the units
                    addVav = False
                else:
                    words.append(units[chunk])

        return " ".join(words)

    # Handle "and" for special cases
    def handle_special_cases(parts):
        result = []
        for i, part in enumerate(parts):
            text = ''
            if part == 0:
                continue
            scale = len(parts) - i - 1
            if scale == 1 and part == 1:
                text = big_numbers[scale]  # "מיליון" and "אלף"
            else:
                text = chunk_to_words(part)
            if scale > 0 and part > 0:
                text = text + " " + big_numbers[scale]
            if i > 0:
                text = "ו" + text
            result.append(text)
        return result

    # Split number into chunks
    parts = chunk_number(num)
    words = handle_special_cases(parts)

    # Join words with correct punctuation
    result = " ".join(words).strip()

    # Fix issues with conjunctions like 'וא'
    result = result.replace("אחד מיליון", "מיליון")
    result = result.replace("אחד אלף", "אלף")
    result = result.replace("שניים אלף", "אלפיים")
    result = result.replace("שתיים אלף", "אלפיים")

    return result
