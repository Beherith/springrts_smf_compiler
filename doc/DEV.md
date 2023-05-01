# PyMapConv Development and Contribution

Follow the guide outlined in README.md to run the software from source.
At this point you are ready to make contributions to the package.

In order to submit a contribution:
1. Fork the repo and make the changes in your fork.
2. Test the build process by running a build script for your operating system.
3. Update the `src/version.py` by bumping the version based on your changes and providing a short release description.
4. Make the Pull Request into master of the root repository.
5. Notify contributors on discord in the #mapping channel.

Additionally, you can leverage the CI/CD scripts provided with the repository to test the release in advance.
When working with the PyMapConv in your fork on github, same CI/CD actions will be ran and the release artifacts will
be produced. It is recommended that you follow a [feature branch workflow](https://www.atlassian.com/git/tutorials/comparing-workflows/feature-branch-workflow)
even in your local repository to verify your release before you merge it into the main repo.

## Testing the build
You will need some additional dependencies to package compiler. Install additional dependencies listed in
`build/requirements-dev.txt`. You can then run the build scripts:
```
# Navigate your shell or command prompt into this repo's build directory
cd springrts_smf_compiler/build

# Install dependencies listed in requirements file
python3 -m pip install -r requirements-dev.txt

# Run the build script for your platform (assuming linux here)
cd linux
./build.sh
```
