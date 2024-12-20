import click
from fireflies_sdk import FirefliesAPI
import os
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

def get_api():
    """Get FirefliesAPI instance using API key from environment"""
    api_key = os.getenv("FIREFLIES_API_KEY")
    if not api_key:
        click.echo("API key not found. Please set it using 'ff config set-key YOUR_API_KEY'")
        exit(1)
    return FirefliesAPI(api_key)

@click.group()
def cli():
    """Fireflies.ai CLI"""
    pass

@cli.group()
def config():
    """Configure the CLI"""
    pass

@config.command("set-key")
@click.argument("api_key")
def set_api_key(api_key):
    """Set your Fireflies API key"""
    try:
        with open(".env", "w") as f:
            f.write(f"FIREFLIES_API_KEY={api_key}\n")
        click.echo("API key saved")
    except Exception as e:
        click.echo(f"Error saving API key: {str(e)}")

@cli.command()
@click.argument("api_key")
def key(api_key):
    """Set your Fireflies API key"""
    try:
        with open(".env", "w") as f:
            f.write(f"FIREFLIES_API_KEY={api_key}\n")
        click.echo("API key saved")
    except Exception as e:
        click.echo(f"Error saving API key: {str(e)}")

@cli.command()
@click.option("--duration", default=120, help="Meeting duration in minutes")
@click.option("--name", help="Name for the bot")
@click.option("--url", help="Meeting URL to join")
def join(duration, name, url):
    """Join a meeting"""
    try:
        api = get_api()
        result = api.join_meeting(duration=duration, name=name, url=url)
        if result.get("success"):
            click.echo("Successfully joined meeting")
            if result.get("message"):
                click.echo(result["message"])
        else:
            click.echo("Failed to join meeting")
    except Exception as e:
        click.echo(f"Error: {str(e)}")

@cli.command()
@click.argument("identifier")
@click.option("-d", "--download", is_flag=True, help="Download the video")
def video(identifier, download):
    """Get video URL for a transcript (use transcript ID)"""
    try:
        api = get_api()
        if download:
            output_path = api.download_video(identifier)
            click.echo(f"Video downloaded successfully to: {output_path}")
        else:
            result = api.get_video_url(identifier)
            click.echo(f"Meeting: {result['title']}")
            click.echo(f"Video URL: {result['video_url']}")
            click.echo("\nNote: This URL expires after 24 hours.")
    except Exception as e:
        click.echo(f"Error: {str(e)}")

@cli.command()
@click.argument("transcript_id")
@click.option("--output", "-o", help="Output file path")
def download(transcript_id, output):
    """Download video for a transcript"""
    try:
        api = get_api()
        output_path = api.download_video(transcript_id, output)
        click.echo(f"Video downloaded to: {output_path}")
    except Exception as e:
        click.echo(f"Error: {str(e)}")

@cli.command()
@click.option("--limit", default=10, help="Maximum number of transcripts to list")
def list(limit):
    """List recent transcripts"""
    try:
        api = get_api()
        click.echo(f"Using API key: {api.api_key}")  # Temporary debug line
        transcripts = api.list_transcripts(limit=limit)
        for t in transcripts:
            date = datetime.fromtimestamp(int(t.get("date", 0))/1000).strftime("%Y-%m-%d %H:%M:%S")
            click.echo(f"{t['id']} - {date} - {t.get('title', 'Untitled')}")
    except Exception as e:
        click.echo(f"Error: {str(e)}")

@cli.command()
@click.argument("transcript_id")
def transcript(transcript_id):
    """Get full transcript text"""
    try:
        api = get_api()
        result = api.get_transcript_text(transcript_id)
        
        # Print transcript info
        title = result.get('title', 'Untitled Meeting')
        click.echo(f"\nTranscript for: {title}\n")
        
        click.echo("Transcript:")
        for sentence in result.get('sentences', []):
            speaker = sentence.get('speaker_name', 'Unknown')
            start_time = sentence.get('start_time', 0)
            text = sentence.get('text', '')
            minutes = int(start_time / 60)
            seconds = int(start_time % 60)
            click.echo(f"[{minutes:02d}:{seconds:02d}] {speaker}: {text}")
    except Exception as e:
        click.echo(f"Error: {str(e)}")

@cli.command()
@click.argument("transcript_id")
def participants(transcript_id):
    """Get meeting participants"""
    try:
        api = get_api()
        participants = api.get_participants(transcript_id)
        
        if not participants:
            click.echo("No participants found")
            return
            
        click.echo("Meeting Participants:")
        for participant in participants:
            click.echo(participant)
    except Exception as e:
        click.echo(f"Error: {str(e)}")

@cli.command()
@click.argument("transcript_id")
def delete(transcript_id):
    """Delete a transcript"""
    try:
        api = get_api()
        if api.delete_transcript(transcript_id):
            click.echo("Transcript deleted successfully")
    except Exception as e:
        click.echo(f"Error: {str(e)}")

if __name__ == "__main__":
    cli()
