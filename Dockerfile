FROM jekyll/jekyll:4.3.0

WORKDIR /srv/jekyll

COPY Gemfile Gemfile.lock ./
RUN bundle install

COPY . .

EXPOSE 4000

CMD ["jekyll", "serve", "--host", "0.0.0.0", "--port", "4000", "--livereload"]
