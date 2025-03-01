import {
    Card,
    CardContent,
    CardDescription,
    CardFooter,
    CardHeader,
    CardTitle,
} from "@/components/ui/card";

import SocialAuthentication from "@/features/auth/SocialAuthentication";
import SignInForm from "./SignInForm";

const SignInCard = () => {
    return (
        <Card className="mx-4 w-[400px] md:w-[400px] lg:w-[450px]">
            <CardHeader>
                <CardTitle>Ready to Continue?</CardTitle>
                <CardDescription>
                    Log in now to continue reading your favorite articles, comment on discussions,
                    and enjoy new content&rsquo;
                </CardDescription>
            </CardHeader>
            <CardContent>
                <SignInForm />
            </CardContent>
            <CardFooter>
                <SocialAuthentication />
            </CardFooter>
        </Card>
    );
};

export default SignInCard;
