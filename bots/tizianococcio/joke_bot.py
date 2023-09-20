from src.presenter import PresenterInterface, NaivePresenter, NarcissusPresenter

class Bot:
    """A bot that can tell jokes and rate the jokes of other bots."""
    def __init__(self, presenter: PresenterInterface, name: str=''):
        self.name = name
        self.presenter = presenter

    def launch_stage(self) -> None:
        """
        Launch the bot's interactive session.
        """
        self.presenter.play()

    def tell_joke(self, style: str = None, mood: str = None) -> str:
        """
        Tell a joke. 

        IMPORTANT: This method is provided as per the description on the GitHub README. It is however
        not directly used to run the interactive session. This is because all the logic for the 
        session is included in the play() method of the Presenter. Since no details were given
        as to how the interactive session should be run, I decided for what seemed a best practice to me,
        i.e.: allowing different types of presenters to be used via implementing an interface.

        Args:
            style: A string containing the style of the joke.
            mood: A string containing the mood of the joke.

        Returns:
            A string containing the joke.
        """
        return self.presenter.generate_joke(style, mood)
    
    def rate_joke(self, joke: str) -> int:
        """
        Rate a joke.

        Args:
            joke: A string containing the joke to be rated.

        Returns:
            An integer between 1 and 10, inclusive, representing the rating of the joke.
        """
        return self.presenter.rate_joke(joke)
