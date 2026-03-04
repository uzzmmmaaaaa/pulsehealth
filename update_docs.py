import re
import sys

html_file = r'c:\Users\uzma\Desktop\online consultation\doctors.html'

try:
    with open(html_file, 'r', encoding='utf-8') as f:
        html = f.read()
except Exception as e:
    print(f"Error opening file: {e}")
    sys.exit(1)

html = re.sub(r'Book Rs\.200 Consult|Book Video Consult|Schedule Consult|Consult Now', 'Consult Now', html)

unique_docs = [
    {'name': 'Dr. Ananya Sharma', 'qual': 'MBBS, MD (Medicine), FACP', 'img': '1559839734-2b71ea197ec2'},
    {'name': 'Dr. Amit Patel', 'qual': 'MBBS, Family Medicine Specialist', 'img': '1622253692010-333f2da6031d'},
    {'name': 'Dr. Neha Gupta', 'qual': 'MBBS, MD (Internal Med), Diabetologist', 'img': '1594824436951-7f126f09bf84'},
    {'name': 'Dr. Rakesh Singh', 'qual': 'MBBS, DNB, General Practice', 'img': '1612349317150-e410f624c427'},
    {'name': 'Dr. Sonia Kapoor', 'qual': 'MBBS, DNB, Advanced Physician', 'img': '1573496359142-b8d87734a5a2'},
    {'name': 'Dr. Rohan Mehta', 'qual': 'MBBS, DPM, Neuropsychiatrist', 'img': '1537368910025-700350fe46c7'},
    {'name': 'Dr. Aisha Khan', 'qual': 'PhD (Clinical Psychology), CBT Expert', 'img': '1580489944761-15a19d654956'},
    {'name': 'Dr. Prakash Iyer', 'qual': 'MBBS, MD (Psychiatry), Addiction Specialist', 'img': '1612276529731-4b21494e6d71'},
    {'name': 'Dr. Meera Das', 'qual': 'MSc (Clinical Psych), Child Behavioral Expert', 'img': '1544005313-94ddf0286df2'},
    {'name': 'Dr. Vivek Sharma', 'qual': 'MBBS, DPM, Geriatric Psychiatrist', 'img': '1600858525892-0bda0ceab3f7'},
    {'name': 'Dr. Priya Patel', 'qual': 'MBBS, MS (OBG), IVF Specialist', 'img': '1551836022-d5d88e9218df'},
    {'name': 'Dr. Sunita Reddy', 'qual': 'MBBS, DGO, High-Risk Pregnancy', 'img': '1527613426441-4da17471b66d'},
    {'name': 'Dr. Kavita Singh', 'qual': 'MBBS, MS, Minimally Invasive Surgeon', 'img': '1588516903720-8ceb67f9ef84'},
    {'name': 'Dr. Anita Desai', 'qual': 'MBBS, MD (OBG), Fetal Medicine', 'img': '1614608682850-e0d6ed316d47'},
    {'name': 'Dr. Maya Nair', 'qual': 'MBBS, DGO, Menopause Specialist', 'img': '1590649880765-91b1956b8276'},
    {'name': 'Dr. Vikram Singh', 'qual': 'MBBS, MD (Pediatrics), Neonatologist', 'img': '1582750433449-648ed1276023'},
    {'name': 'Dr. Shruti Jain', 'qual': 'MBBS, DCH, Pediatric Allergy', 'img': '1605635882583-b9acb88dcbd9'},
    {'name': 'Dr. Tariq Ali', 'qual': 'MBBS, MD, Pediatric Neurology', 'img': '1593032465175-481ac7f401a0'},
    {'name': 'Dr. Karan Kapoor', 'qual': 'MBBS, DNB (Peds), Pulmonology', 'img': '1506794778202-cad84cf45f1d'},
    {'name': 'Dr. Lata M', 'qual': 'MBBS, MD (Pediatrics), Growth Expert', 'img': '1544717305-2782549b5136'}
]

headers = re.split(r'(<div class="doc-card-header">)', html)
new_html = headers[0]
doc_idx = 0
for i in range(1, len(headers) - 1, 2):
    header_tag = headers[i]
    content = headers[i+1]
    
    if doc_idx < len(unique_docs):
        doc = unique_docs[doc_idx]
        new_img = f'<img src="https://images.unsplash.com/photo-{doc["img"]}?ixlib=rb-4.0.3&auto=format&fit=crop&w=300&q=80" alt="{doc["name"]}" class="doc-avatar">\n                        '
        content = re.sub(r'[\s\S]*?(<div class="doc-info-brief">)', new_img + r'\1', content, count=1)
        content = re.sub(r'<h3>.*?</h3>', f'<h3>{doc["name"]}</h3>', content, count=1)
        content = re.sub(r'<span class="doc-qual">.*?</span>', f'<span class="doc-qual">{doc["qual"]}</span>', content, count=1)
        doc_idx += 1
        
    new_html += header_tag + content

# If there's a trailing part after the last matched pair (which shouldn't happen with split properly, but just in case)
if len(headers) % 2 != 0 and len(headers) > 1:
   pass # handled by iteration
if len(headers) % 2 == 1:
    new_html += headers[-1]

with open(html_file, 'w', encoding='utf-8') as f:
    f.write(new_html)

print("Updated doctors.html successfully.")
