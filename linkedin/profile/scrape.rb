require 'linkedin-scraper'

profile = Linkedin::Profile.new("https://www.linkedin.com/in/tuanfeng-wang-3819ab75/")

puts profile.first_name 