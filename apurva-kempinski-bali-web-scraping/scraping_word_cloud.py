from requests import get
from re import sub
from bs4 import BeautifulSoup
from wordcloud import WordCloud, STOPWORDS
from time import perf_counter

def remove_special_characters(review: str):
    review = review.replace("😊","")
    review = review.replace("👍","")
    review = review.replace("’","")
    review = review.replace("!","")
    review = review.replace(".","")
    review = review.replace(")","")
    review = review.replace(",","")
    review = review.replace(":","")
    review = review.replace("-","")
    review = review.replace("'","")
    return review

def correct_typo(review: str):
    review = review.replace("pleasent","pleasant")
    review = review.replace("recomended","recommended")
    review = review.replace("recommend","recommended")
    review = review.replace("exceptionally","exceptional")
    return review

def scrape_reviews():
    scrape_start_time = perf_counter()
    all_reviews = []
    for page in range(1,9):
        page_start_time = perf_counter()
        print(f"Scraping page {page} ...")
        url = f"https://www.booking.com/reviews/id/hotel/the-apurva-kempinski-bali.html?aid=356980&label=gog235jc-1DCA0oaEIZdGhlLWFwdXJ2YS1rZW1waW5za2ktYmFsaUgzWANoaIgBAZgBMbgBF8gBDNgBA-gBAfgBAogCAagCA7gCnNKLogbAAgHSAiRhNTZlZDcxNS0yNTIzLTRmY2QtOTIwMy05MmRhYTVlYzdkOWLYAgTgAgE&sid=d5b706fb1e392d7bdb21e2beb7949c62&customer_type=total&hp_nav=0&old_page=0&order=featuredreviews&page={page}&r_lang=en&rows=75&"

        html_text = get(url).text
        soup = BeautifulSoup(html_text, 'lxml')
        reviews = soup.find_all('div',class_="review_item_header_content")

        for word in reviews:
            try:
                review = word.span.text.strip()
                review = remove_special_characters(review)
                review = correct_typo(review)
                all_reviews.append(review.strip().lower())
            except: pass
        
        page_end_time = perf_counter()

        print(f"Scraping page {page} finished!")
        print(f"Scraping page {page} took {page_end_time-page_start_time:.4f} seconds\n")
    
    scrape_end_time = perf_counter()
    print(f"Scraping took {scrape_end_time-scrape_start_time:.4f} seconds!\n")

    return all_reviews

def clean_reviews(reviews: list): return list(filter(None, reviews))

def convert_review_to_paragraph(reviews: list):
    review_text = " ".join(reviews)
    review_text = sub("  "," ",review_text)
    return review_text

def save_review_to_txt_file(path:str,filename:str):
    all_reviews = clean_reviews(scrape_reviews())
    print("Scraping Apurva Kempinski Bali Reviews From Booking.com Website Finished!")
    review_text = convert_review_to_paragraph(all_reviews)
    with open(path+filename, "w") as text_file: text_file.write(review_text)

def convert_review_to_wordcloud(reviews: str, wordcloud_file_name: str):
    print("Converting Reviews To Wordcloud ...")
    wordcloud_start_time = perf_counter()
    sw = list(STOPWORDS)
    stopwords = list(set([
        "a",
        "overall",
        "place",
        "for",
        "this",
        "internet",
        "icon",
        "hotel",
        "to",
        "yourself",
        "property",
        "place",
        "stay",
        "the",
        "you",
        "should",
        "at",
        "least",
        "once",
        "it",
        "the",
        "very",
        "much",
        "and",
        "one",
        "of",
        "were",
        "really",
        "walk",
        "need",
        "wait",
        "team",
        "think",
        "spend",
        "bit",
        "building",
        "hiccups",
        "ou",
        "deco",
        "dua",
        "peak",
        "complex",
        "decor",
        "koral",
        "every",
        "towards",
        "apurva",
        "extremely",
        "sure",
        "nusa",
        "disa",
        "little",
        "planet",
        "lagoon",
        "cant",
        "go",
        "take",
        "aspect",
        "halls",
        "although",
        "needs",
        "seen",
        "returned",
        "kempinski",
        "ive",
        "penny",
        "look",
        "trip",
        "besides",
        "later",
        "already",
        "long",
        "back",
        "alone",
        "return",
        "staying",
        "come",
        "will",
        "bali",
        "everything",
        "swimming",
        "room",
        "stayed",
        "bed",
        "truly",
        "possibly",
        "welcome",
        "dark",
        "making",
        "improveed",
        "real",
        "thank",
        "better",
        "staff",
        "island",
        "whole",
        "season",
        "going",
        "forward",
        "pools",
        "rooms",
        "check",
        "time",
        "despite",
        "hotels",
        "highly",
        "improve",
        "definitely"
        ]))

    sw.extend(stopwords)
    sw = list(set(sw))

    wc = WordCloud (
        background_color='white',
        stopwords=sw,
    )

    wc.generate(reviews)
    wc.to_file(wordcloud_file_name+'.png')

    wordcloud_end_time = perf_counter()
    print("\nConverting Reviews To WordCloud Finished!")
    print(f"Converting To WordCloud Takes {wordcloud_end_time - wordcloud_start_time:.4f} seconds\n")

def run(path:str,filename:str,wordcloud_file_name:str):
    program_start = perf_counter()
    save_review_to_txt_file(path,filename)
    reviews = open(path+filename,mode='r',encoding='utf-8').read()
    convert_review_to_wordcloud(reviews, wordcloud_file_name)
    program_end = perf_counter()
    print(f"Program Takes {program_end-program_start:.4f} seconds to execute")

if __name__ == '__main__':
    print()
    print("Scraping Apurva Kempinski Bali Reviews From booking.com Website Starting ...\n")
    path = "apurva-kempinski-bali-web-scraping/"
    filename = "review.txt"
    wordcloud_file_name = path+"apurva_kempinski_bali_review_wordcloud"
    run(path,filename,wordcloud_file_name)
    print()