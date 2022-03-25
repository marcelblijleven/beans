set -e

if [[ $(git rev-parse --abbrev-ref HEAD) = "master" ]]; then
  cz bump --changelog
else
  cz bump --changelog --prerelease beta
fi

read -r -p "Do you want to push the tag to the remote? [n/Y]" response

if [[ "$response" =~ ^([yY][eE][sS]|[yY])$ ]]
then
    echo "git push --tags"
else
    echo "You can manually push the tags using 'git push --tags' at a later stage"
fi
