from Utility import remove_emoji

 
def get_post_time_stamp(post):
    # Get Date
    timestamp = ''
    try:
        date_obj = post.find_element_by_css_selector('._5ptz')
        timestamp = date_obj.get_attribute("data-utime")
    except Exception as e:
        print("Error retrieving date " + str(e))

    return timestamp

def get_post_text(post):
    # Post content
    post_text  = ''
    entities = []            
    try: 
        post_text = post.find_element_by_class_name('userContent').text
        clean_emoji = remove_emoji(post_text)
        print(post_text)
        
    except Exception as e:
        print('Issue with retrieving content: ' + str(e))

    return post_text

def get_author_name(post):
    # Author Name
    author_name = ''
    try:
        author_name = post.find_element_by_css_selector('.fwb.fcg a').text         
    except Exception as e:
        print("Error retrieving author name" + str(e))
    return author_name