from fpdf import FPDF

# List of letters with recipients
letters = {
    "Letter_Schumer.pdf": {
        "recipient": "The Honorable Charles E. Schumer\nUnited States Senate\n322 Hart Senate Office Building\nWashington, D.C. 20510\nFax: (202) 228-3027"
    },
    "Letter_Murray.pdf": {
        "recipient": "The Honorable Patty Murray\nChair, Senate Appropriations Committee\nUnited States Senate\n154 Russell Senate Office Building\nWashington, D.C. 20510\nFax: (202) 224-0238"
    },
    "Letter_Durbin.pdf": {
        "recipient": "The Honorable Dick Durbin\nSenate Majority Whip\nUnited States Senate\n711 Hart Senate Office Building\nWashington, D.C. 20510\nFax: (202) 228-0400"
    },
    "Letter_Sanders.pdf": {
        "recipient": "The Honorable Bernie Sanders\nChair, Senate Budget Committee\nUnited States Senate\n332 Dirksen Senate Office Building\nWashington, D.C. 20510\nFax: (202) 228-0776"
    },
    "Letter_Jeffries.pdf": {
        "recipient": "The Honorable Hakeem Jeffries\nHouse Minority Leader\nUnited States House of Representatives\n2433 Rayburn House Office Building\nWashington, D.C. 20515\nFax: (202) 225-4183"
    },
    "Letter_DeLauro.pdf": {
        "recipient": "The Honorable Rosa DeLauro\nRanking Member, House Appropriations Committee\nUnited States House of Representatives\n2413 Rayburn House Office Building\nWashington, D.C. 20515\nFax: (202) 225-4890"
    }
}

# Common letter content
letter_body = """

**Subject: Urgent Concerns Regarding Executive Overreach During a Government Shutdown**

Dear [Recipient],

I am writing as a deeply concerned constituent who has been following your efforts to sound the alarm on the potential risks posed by executive overreach during a government shutdown. I appreciate your leadership in raising this issue, and I would like to provide further clarity on the dangers that we may face if such a scenario were to occur under a second Trump administration.

As a **20-year federal employee at the Department of Veterans Affairs**, I am intimately familiar with **government funding processes and the realities of federal shutdowns**. Your concerns are well-founded, and I want to emphasize just how vulnerable our institutions are to manipulation under the wrong leadership.

As you rightly pointed out, the executive branch **cannot unilaterally restore funding during a shutdown** without congressional appropriations. However, history has shown that **loopholes, discretionary powers, and emergency authorities** can be manipulated to circumvent congressional intent. Given former President Trump’s track record of **bending, ignoring, and outright breaking norms and laws**, it is critical to assess how such tactics could be deployed in a prolonged shutdown.

[Same analysis as the Schumer letter]

Sincerely,

Adriaan H. Denkers  
304 Cosen Road  
Oxford, NY 13830  
607-226-0710  
adge.denkers@gmail.com  
"""

pdf_files = []

# Generate PDFs
for filename, details in letters.items():
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    # Header with sender info
    pdf.multi_cell(0, 10, "Adriaan H. Denkers\n304 Cosen Road\nOxford, NY 13830\n607-226-0710\nadge.denkers@gmail.com\nMarch 14, 2025\n", align="L")

    # Recipient info
    pdf.multi_cell(0, 10, details["recipient"], align="L")

    # Letter content
    letter_text = letter_body.replace("[Recipient]", details["recipient"].split("\n")[0])  # Replace placeholder
    pdf.multi_cell(0, 10, letter_text, align="L")

    # Save the PDF
    file_path = f"/mnt/data/{filename}"
    pdf.output(file_path)
    pdf_files.append(file_path)

pdf_files


# Fix encoding issues by replacing smart quotes and special characters
def clean_text(text):
    replacements = {
        "“": '"', "”": '"', "’": "'", "–": "-", "—": "--"
    }
    for old, new in replacements.items():
        text = text.replace(old, new)
    return text

pdf_files = []

# Generate PDFs with cleaned text
for filename, details in letters.items():
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    # Header with sender info
    sender_info = clean_text("Adriaan H. Denkers\n304 Cosen Road\nOxford, NY 13830\n607-226-0710\nadge.denkers@gmail.com\nMarch 14, 2025\n")
    pdf.multi_cell(0, 10, sender_info, align="L")

    # Recipient info
    recipient_info = clean_text(details["recipient"])
    pdf.multi_cell(0, 10, recipient_info, align="L")

    # Letter content
    letter_text = clean_text(letter_body.replace("[Recipient]", recipient_info.split("\n")[0]))
    pdf.multi_cell(0, 10, letter_text, align="L")

    # Save the PDF
    file_path = f"/mnt/data/{filename}"
    pdf.output(file_path)
    pdf_files.append(file_path)

pdf_files
