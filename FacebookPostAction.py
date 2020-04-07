def click_see_more_button(post):
        try:
            seemore = post.find_element_by_link_text("See more")
            seemore.send_keys(Keys.ENTER)
        except:
            pass