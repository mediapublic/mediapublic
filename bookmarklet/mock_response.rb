require 'sinatra'

if ARGV.length == 0
  puts "ruby mock_response.rb response1 response2 response3 [...]"
  exit
end

before do
   headers 'Access-Control-Allow-Origin' => '*',
            'Access-Control-Allow-Methods' => ['OPTIONS', 'GET', 'POST']
end

set :protection, false

configure do
  enable :sessions
end

$step = 0

post '*' do
  $step = 0 if $step == ARGV.length
  $step += 1
  ARGV[$step - 1]
end
